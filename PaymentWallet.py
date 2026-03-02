import os
import json
import time
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, text
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

@app.get("/health")
def health():
    return {"ok": True}

class JobDTO(BaseModel):
    wallet: str
    amount: float  # human units

class UpdateNodeAttributesDTO(BaseModel):
    api_key: str | None = None
    job_id: int | None = None
    attribute_filters: dict
    new_attributes: dict

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

    # Create job record in DB
    with engine.begin() as conn:
        res = conn.execute(
            text("INSERT INTO jobs (job_type, user_wallet, amount, status) VALUES (:t,:w,:a,'PENDING') RETURNING id"),
            {"t": "STAKE", "w": checksum, "a": units}
        )
        job_id = res.scalar_one()

    # enqueue worker job with job_id
    q.enqueue("worker.process_job", job_id, job_timeout=600)
    return {"job_id": job_id, "status": "queued"}

@app.post("/update_node_attributes")
def update_node_attributes(payload: UpdateNodeAttributesDTO, x_api_key: str = Header(default=None)):
    key_ok = True
    if API_KEY:
        key_ok = (x_api_key == API_KEY) or (payload.api_key == API_KEY)
    if not key_ok:
        raise HTTPException(status_code=401, detail="Invalid API key")
    allowed_cols = {"status", "tx_hash", "amount", "user_wallet", "job_type", "id"}
    filters = {}
    updates = {}
    if payload.job_id is not None:
        filters["id"] = payload.job_id
    for k, v in payload.attribute_filters.items():
        if k in allowed_cols:
            filters[k] = v
    for k, v in payload.new_attributes.items():
        if k in allowed_cols and k != "id":
            updates[k] = v
    if not filters or not updates:
        raise HTTPException(status_code=400, detail="No valid filters or updates")
    where_clause = " AND ".join([f"{k} = :f_{k}" for k in filters])
    set_clause = ", ".join([f"{k} = :u_{k}" for k in updates])
    params = {}
    for k, v in filters.items():
        params[f"f_{k}"] = v
    for k, v in updates.items():
        params[f"u_{k}"] = v
    with engine.begin() as conn:
        res = conn.execute(text(f"UPDATE jobs SET {set_clause} WHERE {where_clause} RETURNING id"), params)
        rows = res.fetchall()
    return {"updated_ids": [r[0] for r in rows]}
