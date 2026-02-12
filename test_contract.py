import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("SERVER_PRIVATE_KEY")
SENDER_ADDRESS = os.getenv("SERVER_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS") # Address from Remix after deployment

# Receiver Wallet (Using Sender Address for testing)
RECEIVER_ADDRESS = os.getenv("SERVER_ADDRESS") 

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Simple ABI for SimpleTransfer contract
ABI = [
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_receiver",
				"type": "address"
			}
		],
		"name": "sendEth",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	}
]

def test_transfer():
    if not CONTRACT_ADDRESS or CONTRACT_ADDRESS == "0x0000000000000000000000000000000000000000":
        print("Error: Please set CONTRACT_ADDRESS in your .env file after deploying via Remix.")
        return

    print(f"Testing transfer through contract: {CONTRACT_ADDRESS}")
    
    # Initialize contract
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)
    
    # Amount to send (e.g., 0.001 Sepolia ETH)
    amount_in_ether = 0.001
    amount_in_wei = w3.to_wei(amount_in_ether, 'ether')
    
    try:
        # Build transaction
        nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
        
        tx = contract.functions.sendEth(
            Web3.to_checksum_address(RECEIVER_ADDRESS)
        ).build_transaction({
            'from': SENDER_ADDRESS,
            'value': amount_in_wei,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        
        # Send transaction
        print("Sending transaction...")
        # Try both common attribute names for compatibility
        raw_tx = getattr(signed_tx, 'rawTransaction', getattr(signed_tx, 'raw_transaction', None))
        if raw_tx is None:
            raise AttributeError(f"Could not find raw transaction in {type(signed_tx)}. Available: {dir(signed_tx)}")
            
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        
        print(f"Success! Transaction Hash: {tx_hash.hex()}")
        print(f"Check status on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_transfer()
