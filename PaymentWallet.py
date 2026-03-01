import os
import json
import time
from decimal import Decimal
from fastapi import FastAPI, HTTPException
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
def request_stake(dto: JobDTO):
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
