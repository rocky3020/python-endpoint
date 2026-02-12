# Supabase & Redis Setup Guide (Hinglish)

Haan bilkul! Aap **Supabase** ko as a database use kar sakte hain kyunki Supabase piche (backend) mein **PostgreSQL** hi use karta hai. Aur Redis ke liye bhi hamare paas kaafi options hain.

---

### 1. Supabase ko kaise use karein?

Supabase ko connect karna bahut simple hai kyunki hamara project pehle se hi **SQLAlchemy** use kar raha hai.

**Steps:**
1. [Supabase](https://supabase.com/) par account banayein aur naya project create karein.
2. Project Settings -> Database mein jayein.
3. Wahan aapko **Connection String** milegi (URI mode mein). Woh kuch aisi dikhegi:
   `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-ID].supabase.co:5432/postgres`
4. Is URL ko apni `.env` file mein `DATABASE_URL` ki jagah daal dein.

**Note:** Password mein special characters hain toh unhe encode karna pad sakta hai, ya fir Supabase ka "Connection Pooling" (Port 6543) use karein agar aap serverless environment mein hain.

---

### 2. Redis ka kya karein?

Redis ka use is project mein **Task Queue (RQ)** ke liye ho raha hai. Iske bina background jobs nahi chalenge. Aapke paas 2 main options hain:

#### Option A: Upstash (Recommended for Supabase users)
Agar aap cloud database (Supabase) use kar rahe ho, toh Redis bhi cloud wala use karna sahi rahega.
1. [Upstash](https://upstash.com/) par jayein (Yeh free tier deta hai).
2. Ek Redis instance banayein.
3. Aapko ek `REDIS_URL` milegi, jaise: `redis://default:yourpassword@your-endpoint.upstash.io:6379`
4. Ise apni `.env` file mein daal dein.

#### Option B: Local Redis (For Testing)
Agar aap apne computer par test kar rahe ho:
- **Mac:** `brew install redis` fir `brew services start redis`.
- **Docker:** `docker run -p 6379:6379 redis`.
- `.env` mein dalo: `REDIS_URL=redis://localhost:6379/0`

---

### Updated `.env` Example for Supabase + Upstash

```env
# Supabase Connection
DATABASE_URL=postgresql://postgres:your_password@db.xyz.supabase.co:5432/postgres

# Upstash/Redis Connection
REDIS_URL=redis://default:your_redis_password@your-endpoint.io:6379

# Blockchain Config
RPC_URL=https://...
SERVER_PRIVATE_KEY=0x...
CONTRACT_ADDRESS=0x...
```

### Table Kaise Banayein?
Supabase ke dashboard mein "SQL Editor" mein jayein aur yeh query run karein:

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_type TEXT,
    user_wallet TEXT,
    amount BIGINT,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

### Kya change karna hoga code mein?
Aapko code mein kuch bhi change karne ki zarurat nahi hai! Kyunki hum **SQLAlchemy** use kar rahe hain, woh apne aap Supabase (Postgres) se baat kar lega. Bas `.env` file update karni hai.
