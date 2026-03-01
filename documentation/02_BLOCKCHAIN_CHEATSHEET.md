# Blockchain & Web3 Cheatsheet (Hinglish)

Yeh cheatsheet aapko is project mein use hone wale technical words ko aasaan bhasha mein samjhayegi.

---

### 1. **Blockchain**
Blockchain ek digital register ya "ledger" hai. Jaise ek dukan ka khata hota hai, waise hi isme saare transactions record hote hain. Iski khaas baat yeh hai ki ise koi hack ya delete nahi kar sakta kyunki yeh kisi ek computer par nahi, balki hazaron computers par chalta hai.

### 2. **Web3**
Internet ka naya version! Web2 mein Google/Facebook ka control hota hai, lekin Web3 mein control "users" ke paas hota hai. Isme blockchain technology ka use hota hai.

### 3. **Smart Contract**
Yeh ek digital agreement hai. Socho ek machine hai jisme aap 10 rupaye daalte ho aur chocolate bahar aati hai—isme kisi insaan ki zarurat nahi hai. Smart Contract bhi waise hi code se chalta hai; jab conditions poori hoti hain, toh transaction apne aap ho jata hai.

### 4. **ABI (Application Binary Interface)**
ABI ek "translator" ki tarah hai. Hamara Python code blockchain ki bhasha nahi samajhta. ABI (ek JSON file) batati hai ki smart contract ke functions ko kaise call karna hai aur data kaise bhejna hai.

### 5. **RPC URL**
RPC URL ek "bridge" (pool) hai. Hamare server ko blockchain network (jaise Ethereum ya Polygon) se baat karne ke liye ek internet link chahiye hota hai, wahi RPC URL hai.

### 6. **Wallet Address vs Private Key**
- **Wallet Address:** Yeh aapka "Bank Account Number" hai. Aap ise kisi ko bhi de sakte ho paise receive karne ke liye. (Example: `0x123...`)
- **Private Key:** Yeh aapka "Password" ya locker ki "Chabi" hai. Ise kabhi kisi ko nahi dikhana chahiye! Isse transactions "sign" hote hain. Agar kisi ke paas yeh key hai, toh woh aapka saara paisa nikal sakta hai.

### 7. **Gas Price & Nonce**
- **Gas Price:** Blockchain par transaction karne ki fees. Network par jitni bheed hogi, Gas Price utna hi badh jayega.
- **Nonce:** Yeh ek simple counter hai. Yeh track karta hai ki ek wallet se kitne transactions hue hain, taaki transactions line se (in order) chalein.

### 8. **SQLAlchemy**
Yeh Python ki ek library hai jo Database (SQL) se baat karti hai. Iska fayda yeh hai ki humein lambi-lambi SQL queries likhne ki zarurat nahi padti, hum Python code se hi data save aur read kar sakte hain.

### 9. **FastAPI & Pydantic**
- **FastAPI:** Ek framework hai API banane ke liye (jaise endpoints: `/request/stake`). Yeh bahut fast hai.
- **Pydantic:** Yeh check karta hai ki jo data user ne bheja hai woh sahi hai ya nahi. Jaise agar "amount" number hona chahiye, toh Pydantic check karega ki user ne text toh nahi bhej diya.

### 10. **Redis & RQ (Redis Queue)**
Blockchain transactions kabhi-kabhi time lete hain. Hum user ko wait nahi karwana chahte.
- **Redis:** Ek super-fast memory storage hai.
- **RQ:** Yeh ek "Waiting List" system hai. Hum transaction ko list mein daal dete hain aur piche (background mein) worker use process karta rehta hai.

---

### Further Process (Aage kya karein?)
Is project ko chalane ke liye:
1. **.env file** banao aur usme saari keys dalo.
2. **contract_abi.json** file project mein rakho.
3. **Database** mein `jobs` table banao.
4. **Worker** start karo (`rq worker`) taaki blockchain transactions background mein chal sakein.
