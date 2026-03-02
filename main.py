from PaymentWallet import app as app

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}
