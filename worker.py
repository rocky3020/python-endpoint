import os
import json
import time
from redis import Redis
from rq import Worker, Queue
from sqlalchemy import create_engine, text
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("SERVER_PRIVATE_KEY")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Initialize DB Engine
engine = create_engine(DATABASE_URL)

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Load ABI
with open("contract_abi.json", "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS) if CONTRACT_ADDRESS and CONTRACT_ADDRESS != "0x0000000000000000000000000000000000000000" else None, abi=abi)

def process_job(job_id):
    """
    This function is called by the RQ worker to process a job.
    """
    print(f"--- Starting Job ID: {job_id} ---")
    
    # 1. Fetch job from DB
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT * FROM jobs WHERE id = :id"),
            {"id": job_id}
        ).fetchone()
        
        if not res:
            print(f"Job {job_id} not found in database.")
            return

    # Job data
    # res index: 0:id, 1:job_type, 2:user_wallet, 3:amount, 4:status, 5:tx_hash, 6:created_at
    user_wallet = res[2]
    amount_wei = int(res[3])
    
    try:
        # 2. Update status to IN_PROGRESS
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET status = 'IN_PROGRESS' WHERE id = :id"),
                {"id": job_id}
            )

        # 3. Prepare Blockchain Transaction
        # For this test, we assume the user_wallet is 'addrA' and we use placeholders for B and C
        # Or if it's a simple transfer, we do that. 
        # Since we have the 'distribute' ABI, let's use it.
        
        # NOTE: You need to provide real addresses for B and C for the percentage split
        addrB = "0x0000000000000000000000000000000000000000" # Replace with real address
        addrC = "0x0000000000000000000000000000000000000000" # Replace with real address

        # Build transaction
        tx = contract.functions.distribute(
            Web3.to_checksum_address(user_wallet),
            Web3.to_checksum_address(addrB),
            Web3.to_checksum_address(addrC)
        ).build_transaction({
            'from': SERVER_ADDRESS,
            'value': amount_wei,
            'nonce': w3.eth.get_transaction_count(SERVER_ADDRESS),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })

        # 4. Sign and Send
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hex = tx_hash.hex()
        
        print(f"Transaction Sent! Hash: {tx_hex}")

        # 5. Update status to COMPLETED
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET status = 'COMPLETED', tx_hash = :h WHERE id = :id"),
                {"h": tx_hex, "id": job_id}
            )
        print(f"Job {job_id} completed successfully.")

    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        # Update status to FAILED
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET status = 'FAILED' WHERE id = :id"),
                {"id": job_id}
            )

def run_worker():
    if not REDIS_URL:
        print("Error: REDIS_URL not found in .env file")
        return

    print(f"Connecting to Redis for Worker... (SSL Fix Enabled)")
    
    try:
        # Connect to Redis with SSL fix
        redis_conn = Redis.from_url(REDIS_URL, ssl_cert_reqs=None)
        
        # Start the worker (Updated for rq 2.x)
        worker = Worker(['chain-jobs'], connection=redis_conn)
        print("Worker is listening for jobs on 'chain-jobs' queue...")
        worker.work()
    except Exception as e:
        print(f"Error starting worker: {e}")

if __name__ == '__main__':
    run_worker()
