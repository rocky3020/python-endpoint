# Database Setup Guide (Hinglish)

Is project mein hum **PostgreSQL** ya **SQLite** ka use kar sakte hain. 

### Konsa Database use karein?

1. **SQLite (Recommended for Development):**
   - **Kyun?** Iske liye aapko koi alag se software install nahi karna padta. Yeh ek simple file hoti hai jo aapke project folder mein hi rehti hai.
   - **Setup:** Bas `DATABASE_URL=sqlite:///./blockchain_jobs.db` set karna hota hai.

2. **PostgreSQL (Recommended for Production):**
   - **Kyun?** Yeh bahut fast aur secure hai. Jab aapka project live jayega, tab yeh best hai.
   - **Setup:** Aapko Postgres install karna padega aur ek database create karna padega.

---

### Step-by-Step Setup (Using SQLite for ease)

#### 1. Database Table Structure (Schema)
Aapko database mein ek `jobs` table banana padega. Is table mein blockchain ke saare transactions track honge.

Run this SQL command in your database:

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_type VARCHAR(50),      -- Example: 'STAKE'
    user_wallet VARCHAR(100),  -- Wallet address
    amount BIGINT,             -- Amount in token units
    status VARCHAR(20),        -- PENDING, COMPLETED, FAILED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. `.env` File Setup
Aapne jo [PaymentWallet.py](file:///Users/arbazkudekar/Downloads/python_script/PaymentWallet.py) dekha tha, woh environment variables se data uthata hai. 

Apne project root mein ek `.env` file banao aur usme yeh dalo:

```env
# Database Configuration
# Agar SQLite use kar rahe ho:
DATABASE_URL=sqlite:///./blockchain_jobs.db

# Agar PostgreSQL use kar rahe ho (example):
# DATABASE_URL=postgresql://username:password@localhost:5432/db_name

# Other Configs
REDIS_URL=redis://localhost:6379/0
RPC_URL=https://your-rpc-url-here
TOKEN_DECIMALS=18
TOKEN_ADDRESS=0x...
SERVER_PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=0x...
```

#### 3. Database Initialization Script
Aap ek chota sa Python script bhi use kar sakte ho table banane ke liye:

```python
# init_db.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

create_table_query = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_type TEXT,
    user_wallet TEXT,
    amount BIGINT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))
    print("Database table 'jobs' created successfully!")
```

---

### Aage kya karna hai?
1. **Pip Install:** Pehle `pip install sqlalchemy psycopg2-binary python-dotenv` run karein.
2. **Run Init Script:** `python init_db.py` run karein taaki database file aur table ban jaye.
3. **Start API:** Uske baad hi [PaymentWallet.py](file:///Users/arbazkudekar/Downloads/python_script/PaymentWallet.py) sahi se chalega.
