# Project Overview: Blockchain Integration Service

This project consists of a set of Python scripts designed to facilitate interactions between a web server and a blockchain smart contract. It includes features for handling payment requests, queueing jobs, and triggering both manual and scheduled blockchain transactions.

---

## File Analysis

### 1. [PaymentWallet.py](file:///Users/arbazkudekar/Downloads/python_script/PaymentWallet.py)
**What it does:**
Acts as the entry point for staking/payment requests. It's a FastAPI application that receives requests, stores them in a database, and queues them for background processing.

**Key Features:**
- **API Endpoint:** `/request/stake` - Receives wallet addresses and amounts.
- **Database Integration:** Uses SQLAlchemy to record jobs in a `jobs` table with a `PENDING` status.
- **Task Queue:** Uses Redis and RQ (Redis Queue) to offload the actual blockchain processing to a worker.
- **Unit Conversion:** Converts human-readable amounts to blockchain token units (based on `TOKEN_DECIMALS`).

**Use Case:**
When a user wants to stake tokens, this script handles the initial request, ensures it's logged, and puts it in a queue so the server doesn't have to wait for the blockchain transaction to complete.

---

### 2. [RegisterServerSmartContract.py](file:///Users/arbazkudekar/Downloads/python_script/RegisterServerSmartContract.py)
**What it does:**
Contains the core logic for sending a transaction to a smart contract to record an action.

**Key Features:**
- **API Endpoint:** `/process/to-blockchain`.
- **Blockchain Interaction:** Uses `web3.py` to call the `recordAction` function on a smart contract.
- **Transaction Signing:** Signs the transaction using a server-side private key before broadcasting it to the network.

**Use Case:**
Used to programmatically register or record data on the blockchain from the server's authority.

---

### 3. [ServerToConnectSmartContract.py](file:///Users/arbazkudekar/Downloads/python_script/ServerToConnectSmartContract.py)
**What it does:**
A configuration and initialization script for connecting to a smart contract.

**Key Features:**
- **Web3 Initialization:** Sets up the connection to an Ethereum-compatible RPC provider.
- **Contract Instance:** Loads the contract ABI from a JSON file and creates a contract object for other scripts to use.
- **Credential Management:** Loads the server's private key from environment variables.

**Use Case:**
Serves as a template or a base configuration for other scripts that need to communicate with the smart contract.

---

### 4. [ServerTriggeredBlockchainTransaction.py](file:///Users/arbazkudekar/Downloads/python_script/ServerTriggeredBlockchainTransaction.py)
**What it does:**
A more advanced version of the blockchain interaction script that supports both manual triggers and automated background tasks.

**Key Features:**
- **Manual Trigger:** `/trigger` endpoint to send a specific transaction on demand.
- **Automated Scheduler:** An asynchronous task (`scheduler`) that runs every 30 seconds to perform periodic blockchain actions automatically.
- **Startup Task:** Automatically starts the scheduler when the FastAPI application launches.

**Use Case:**
Ideal for systems that require periodic "heartbeats" or automated updates to the blockchain without manual intervention.

---

## Further Processes to Do

To make this project fully functional, the following steps are required:

### 1. Missing Files & Configuration
- **Create `.env` File:** You must provide a `.env` file with the following variables:
  - `RPC_URL`: Your blockchain provider URL.
  - `REDIS_URL`: Connection string for your Redis server.
  - `DATABASE_URL`: Connection string for your PostgreSQL/SQL database.
  - `SERVER_PRIVATE_KEY`: The private key for the server wallet.
  - `CONTRACT_ADDRESS`: The deployed address of your smart contract.
  - `TOKEN_ADDRESS`: (If applicable) The ERC-20 token address.
- **Provide `contract_abi.json`:** This file is missing. You need to export the ABI from your compiled smart contract and place it in the project root.

### 2. Infrastructure Setup
- **Database Table:** Create the `jobs` table in your database. It should include:
  - `id` (Primary Key)
  - `job_type` (e.g., 'STAKE')
  - `user_wallet` (String/Address)
  - `amount` (BigInt/Numeric)
  - `status` (e.g., 'PENDING', 'COMPLETED', 'FAILED')
- **Redis Server:** Ensure a Redis instance is running for the RQ task queue.

### 3. Implement the Worker
- **`worker.py`:** Create a worker script that listens to the `chain-jobs` queue and implements the `process_job` function. This function should:
  1. Fetch the job from the DB.
  2. Execute the blockchain transaction.
  3. Update the job status in the DB to `COMPLETED` or `FAILED`.

### 4. Dependencies
Install the required Python packages:
```bash
pip install fastapi uvicorn web3 sqlalchemy redis rq python-dotenv pydantic
```

### 5. Running the Application
Start the API server:
```bash
uvicorn PaymentWallet:app --reload
```
And in a separate process, start the worker:
```bash
rq worker chain-jobs
```
