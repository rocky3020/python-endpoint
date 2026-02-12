# Receiver Guide: How to Get Tokens in Your Wallet (Hinglish)

Agar aap **Receiver** hain aur aap chahte hain ki tokens aapke wallet mein aayein, toh is project ka logic samajhna zaroori hai. 

Blockchain mein do tarah se tokens milte hain: **Push** (Server bhejta hai) aur **Pull** (Aap claim karte ho). Is project ka current code **Push** logic par based hai.

---

### 1. Token Receive karne ka Process

Current scripts (jaise [ServerTriggeredBlockchainTransaction.py](file:///Users/arbazkudekar/Downloads/python_script/documentation/01_PROJECT_DOCUMENTATION.md)) mein server ek transaction trigger karta hai.

**Aapko kya karna hoga:**
1. **Wallet Address Share Karein:** Aapko apna wallet address (e.g., `0x123...`) server ko dena hoga.
2. **Server Trigger:** Server jab API endpoint `/trigger` ya `/request/stake` ko call karega, toh woh background mein smart contract ka `recordAction` ya `transfer` function call karega.
3. **Transaction Signing:** Server apni **Private Key** use karke transaction sign karega aur gas fees pay karega. 
4. **Token Credit:** Jaise hi transaction blockchain par confirm hoga, tokens aapke wallet balance mein dikhne lagenge.

---

### 2. Code mein Receiver kaise set karein?

Agar aap chahte hain ki specific amount aapke wallet mein aaye, toh aapko code mein `user` parameter mein apna address pass karna hoga.

**Example (API Request):**
Agar aap `/trigger` endpoint use kar rahe hain, toh request aisi dikhegi:
```json
{
  "user": "YOUR_WALLET_ADDRESS_HERE",
  "amount": 100
}
```

---

### 3. Receiver ke liye Important Tips (Hinglish)

- **Gas Fees:** Is project mein server transaction trigger kar raha hai, iska matlab **Gas Fees server pay karega**, aapko (receiver ko) kuch pay karne ki zarurat nahi hai.
- **Wallet Check:** Aap apne wallet (Metamask, Trust Wallet) mein jaakar check kar sakte hain. Agar tokens nahi dikh rahe, toh "Import Token" par click karke contract address daalna pad sakta hai.
- **Smart Contract Function:** Dhyan rahe ki smart contract mein `recordAction` ya `transfer` function receiver ke address ko accept karta ho.

---

### 4. Aage kya badlav kar sakte hain? (Enhancements)
Agar aap chahte hain ki user khud "Claim" kare (Pull method):
1. Smart Contract mein ek `claimTokens` function banana padega.
2. User ko apne wallet se transaction sign karna padega aur gas fees deni padegi.
3. Yeh method zyada secure hota hai bade projects ke liye.
