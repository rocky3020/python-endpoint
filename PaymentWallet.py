import os
import json
import time
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Any, Dict
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from redis import Redis
from rq import Queue
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Config
RPC_URL = os.getenv("RPC_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_DECIMALS = int(os.getenv("TOKEN_DECIMALS", "18"))
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
API_KEY = os.getenv("API_KEY")

# DB (SQLAlchemy core minimal)
engine = create_engine(DATABASE_URL, future=True)

# Redis + RQ (ssl_cert_reqs=None is used to fix macOS SSL issues with Upstash)
redis_conn = Redis.from_url(REDIS_URL, ssl_cert_reqs=None)
q = Queue("chain-jobs", connection=redis_conn, default_timeout=600)

# Web3 provider (for read-only if needed)
w3 = Web3(Web3.HTTPProvider(RPC_URL))

app = FastAPI()

class JobDTO(BaseModel):
    wallet: str
    amount: float  # human units

def to_token_units(amount: float) -> int:
    factor = 10 ** TOKEN_DECIMALS
    return int(Decimal(amount) * factor)

@app.post("/request/stake")
def request_stake(dto: JobDTO, x_api_key: str = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    try:
        checksum = w3.to_checksum_address(dto.wallet)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid address")

    units = to_token_units(dto.amount)

    try:
        with engine.begin() as conn:
            res = conn.execute(
                text("INSERT INTO jobs (job_type, user_wallet, amount, status) VALUES (:t,:w,:a,'PENDING') RETURNING id"),
                {"t": "STAKE", "w": checksum, "a": units}
            )
            job_id = res.scalar_one()
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")

    q.enqueue("worker.process_job", job_id, job_timeout=600)
    return {"job_id": job_id, "status": "queued"}

class UpdateNodeAttributesDTO(BaseModel):
    api_key: Optional[str] = None
    job_id: Optional[int] = None
    attribute_filters: Optional[Dict[str, Any]] = None
    new_attributes: Dict[str, Any]

@app.post("/update_node_attributes")
def update_node_attributes(payload: UpdateNodeAttributesDTO, x_api_key: str = Header(default=None)):
    if API_KEY and not (x_api_key == API_KEY or payload.api_key == API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API key")
    allowed = {"status", "tx_hash", "amount", "job_type", "user_wallet"}
    updates = {k: v for k, v in payload.new_attributes.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="No updatable fields provided")
    conditions = []
    params: Dict[str, Any] = {}
    if payload.job_id is not None:
        conditions.append("id = :id")
        params["id"] = payload.job_id
    if payload.attribute_filters:
        for k, v in payload.attribute_filters.items():
            if k in allowed or k == "id":
                conditions.append(f"{k} = :f_{k}")
                params[f"f_{k}"] = v
    if not conditions:
        raise HTTPException(status_code=400, detail="No filter provided")
    set_parts = []
    for k, v in updates.items():
        set_parts.append(f"{k} = :u_{k}")
        params[f"u_{k}"] = v
    sql = f"UPDATE jobs SET {', '.join(set_parts)} WHERE {' AND '.join(conditions)}"
    try:
        with engine.begin() as conn:
            res = conn.execute(text(sql), params)
            count = res.rowcount if res is not None else 0
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"updated_rows": count}
