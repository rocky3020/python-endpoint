@app.post("/process/to-blockchain")
def send_to_blockchain(data: dict):
 

    tx = contract.functions.recordAction(
        data["user"],
        data["value"]
    ).build_transaction({
        "from": SERVER_ADDRESS,
        "nonce": w3.eth.get_transaction_count(SERVER_ADDRESS),
        "gasPrice": w3.eth.gas_price,
    })

    signed = w3.eth.account.sign_transaction(tx, SERVER_WALLET)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    return {"transaction_hash": tx_hash.hex()}
