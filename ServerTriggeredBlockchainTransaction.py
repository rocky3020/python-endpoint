from fastapi import FastAPI
from web3 import Web3
import json, os, asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

RPC = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("SERVER_PRIVATE_KEY")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")

w3 = Web3(Web3.HTTPProvider(RPC))

# Contract yükle
with open("contract_abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

# Sunucuda otomatik gönderilecek fonksiyon
def send_to_chain(user, amount):
    tx = contract.functions.recordAction(user, amount).build_transaction({
        "from": SERVER_ADDRESS,
        "nonce": w3.eth.get_transaction_count(SERVER_ADDRESS),
        "gasPrice": w3.eth.gas_price,
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

# ENDPOINT — manuel tetikleme
@app.post("/trigger")
def trigger(data: dict):
    """
    Örnek DTO:
    {
      "user": "0x12...",
      "amount": 100
    }
    """
    result = send_to_chain(data["user"], data["amount"])
    return {"tx": result}

# CRON / Event Tetikleyici (otomatik işlemler)
async def scheduler():
    while True:
        # örnek: her 30 saniyede bir otomatik zincir işlemi
        send_to_chain("0x000000...", 1)
        await asyncio.sleep(30)

@app.on_event("startup")
async def start_tasks():
    asyncio.create_task(scheduler())
