# Production Deployment Guide (Hinglish)

Is project ko real world mein deploy karne ke liye aapko niche diye gaye steps follow karne honge. Yeh guide project ko secure aur stable banane mein help karegi.

---

### Phase 1: Infrastructure Setup

#### 1. Database (Supabase)
- **Project Create Karein:** [Supabase](https://supabase.com/) par naya project banayein.
- **Table Banayein:** SQL Editor mein jaakar `jobs` table create karein (Refer to `04_SUPABASE_REDIS_GUIDE.md`).
- **Connection String:** Project Settings -> Database se Connection String (URI) copy karein.

#### 2. Redis (Upstash)
- **Instance Banayein:** [Upstash](https://upstash.com/) par Redis database banayein.
- **URL Copy Karein:** `REDIS_URL` ko copy karein.

#### 3. Blockchain (RPC Provider)
- **Alchemy/Infura:** [Alchemy](https://www.alchemy.com/) ya Infura par account banayein.
- **Mainnet/Testnet URL:** Real deployment ke liye Mainnet URL lein, testing ke liye Sepolia/Mumbai use karein.

---

### Phase 2: Environment Configuration

Ek `.env` file banayein server par (Ise GitHub par upload NA karein):

```env
# Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[ID].supabase.co:5432/postgres

# Redis
REDIS_URL=redis://default:[PASSWORD]@your-endpoint.io:6379

# Blockchain
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-api-key
CONTRACT_ADDRESS=0x...
TOKEN_ADDRESS=0x...
TOKEN_DECIMALS=18

# Security (Bohot important!)
SERVER_PRIVATE_KEY=your_real_private_key
SERVER_ADDRESS=0xyour_server_wallet_address
```

---

### Phase 3: Server Deployment (Render/DigitalOcean/AWS)

Aap **Render.com** ya **Railway.app** jaise platforms use kar sakte hain kyunki woh bahut aasaan hain.

#### 1. Project Structure
Aapka GitHub repo aisa dikhna chahiye:
```text
/
├── documentation/
├── PaymentWallet.py
├── worker.py (Aapko yeh banana hoga)
├── requirements.txt
└── .env (Strictly ignored by .gitignore)
```

#### 2. Worker Setup (The Missing Piece)
Production mein background jobs ke liye aapko ek `worker.py` file chahiye:
```python
import os
from redis import Redis
from rq import Worker, Queue
from dotenv import load_dotenv

load_dotenv()

# macOS SSL Fix: Agar aapko 'CERTIFICATE_VERIFY_FAILED' error aaye, 
# toh ssl_cert_reqs=None use karein:
conn = Redis.from_url(os.getenv("REDIS_URL"), ssl_cert_reqs=None)

if __name__ == '__main__':
    queues = [Queue('chain-jobs', connection=conn)]
    worker = Worker(queues, connection=conn)
    worker.work()
```

#### 3. Deployment Commands
- **API Server:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker PaymentWallet:app`
- **Background Worker:** `python worker.py`

---

### Phase 4: Security Checklist (Hinglish)

1. **Private Key Protection:** Kabhi bhi Private Key code mein hardcode na karein. Hamesha Environment Variables use karein.
2. **Wallet Funding:** Server wallet mein hamesha thoda extra ETH rakhein gas fees ke liye.
3. **Database Indexing:** Agar jobs table badi ho jaye, toh `user_wallet` aur `status` par indexes lagayein taaki search fast ho.
4. **Rate Limiting:** Apne API par limit lagayein taaki koi spam na kar sake.
5. **Monitoring:** Alchemy ya Infura ke dashboard par transaction failures check karte rahein.

---

### Summary of Deployment Steps

1. **Supabase** aur **Upstash** setup karein.
2. **GitHub** par code push karein (lekin `.env` aur keys hide rakhein).
3. **Render/Railway** par do services banayein:
   - Ek Web Service (API ke liye).
   - Ek Background Worker (Blockchain transactions ke liye).
4. **Environment Variables** platform ke dashboard par add karein.
5. **Deploy!**

Maine yeh guide **[08_PRODUCTION_DEPLOYMENT.md](file:///Users/arbazkudekar/Downloads/python_script/documentation/08_PRODUCTION_DEPLOYMENT.md)** ke naam se save kar di hai.
