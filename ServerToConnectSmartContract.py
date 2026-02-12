from fastapi import FastAPI
from web3 import Web3
import json, os

app = FastAPI()

w3 = Web3(Web3.HTTPProvider("https://provider adress/eth"))

with open("contract_abi.json") as f:
    abi = json.load(f)

contract_address = "0xYourContract"
contract = w3.eth.contract(address=contract_address, abi=abi)

SERVER_WALLET = os.getenv("SERVER_PRIVATE_KEY")
SERVER_ADDRESS = "0xYourServerAddress"
