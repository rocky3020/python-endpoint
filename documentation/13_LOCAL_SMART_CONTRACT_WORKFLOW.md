# Local Smart Contract Development & Deployment Guide

This guide explains how to use the `local_blockchain_project` folder to write, test, and deploy your smart contracts.

## 1. Writing Your Contract
-   **Where:** Put your `.sol` files in the `contracts/` folder.
-   **Example:** [SimpleTransfer.sol](file:///Users/arbazkudekar/Downloads/python_script/local_blockchain_project/contracts/SimpleTransfer.sol) is already there.

## 2. Compiling
Before testing or deploying, you must compile your code:
```bash
npx hardhat compile
```
This checks for errors and creates the **ABI** and **Bytecode** in the `artifacts/` folder.

## 3. Testing (Local)
Always test your code locally to save gas and time.
-   **Where:** Put your test scripts in the `test/` folder.
-   **Run Tests:**
    ```bash
    npx hardhat test
    ```
-   **Local Node:** You can also run a dedicated local node to see transaction logs:
    ```bash
    npx hardhat node
    ```

## 4. Deploying
### A. To Local Network (Fast & Free)
1.  Start the node: `npx hardhat node`
2.  Deploy:
    ```bash
    npx hardhat run scripts/deploy.js --network localhost
    ```

### B. To Sepolia Testnet (Real Test)
1.  Ensure your `.env` has `RPC_URL` and `SERVER_PRIVATE_KEY`.
2.  Deploy:
    ```bash
    npx hardhat run scripts/deploy.js --network sepolia
    ```

## 5. Summary of Workflow
1.  **Code** (in `contracts/`)
2.  **Compile** (`npx hardhat compile`)
3.  **Test** (`npx hardhat test`)
4.  **Deploy** (`npx hardhat run scripts/deploy.js`)

## Important Tip
If you get a **Permission Denied (EPERM)** error on macOS, run this command once to fix Hardhat's settings folder:
```bash
mkdir -p "/Users/arbazkudekar/Library/Preferences/hardhat-nodejs" && echo '{"consent": false}' > "/Users/arbazkudekar/Library/Preferences/hardhat-nodejs/telemetry-consent.json"
```
