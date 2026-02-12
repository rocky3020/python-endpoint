# Simple Contract Deployment & Test Guide (Hinglish)

Agar aap blockchain par ek simple transaction test karna chahte hain, toh yeh guide aapke liye sabse best hai. Hum ek **SimpleTransfer** contract use karenge jo sirf paisa (ETH) leta hai aur use dusre wallet mein bhej deta hai.

---

### **Step 1: Contract Code Likhein**

Maine aapke liye **[SimpleTransfer.sol](file:///Users/arbazkudekar/Downloads/python_script/SimpleTransfer.sol)** file bana di hai. Iska code bahut simple hai:

```solidity
function sendEth(address payable _receiver) public payable {
    require(msg.value > 0, "Amount 0 nahi ho sakta");
    _receiver.transfer(msg.value);
}
```

---

### **Step 2: Remix IDE se Deploy Karein (Sabse Easy Tarika)**

1.  **[Remix IDE](https://remix.ethereum.org/)** par jayein.
2.  Ek nayi file banayein: `SimpleTransfer.sol`.
3.  Mera diya hua code usme paste karein.
4.  **Compile:** Left side mein 'Solidity Compiler' icon par click karein aur `Compile SimpleTransfer.sol` button dabayein.
5.  **Deploy:** 'Deploy & Run Transactions' icon par click karein.
    -   **Environment:** 'Injected Provider - MetaMask' select karein (Make sure aap Sepolia Testnet par hain).
    -   **Deploy:** Orange color ka `Deploy` button dabayein.
6.  MetaMask mein transaction confirm karein. Deployment ke baad aapko niche `Deployed Contracts` mein apna address mil jayega.

---

### **Step 3: Contract ko Test Kaise Karein?**

Aap Remix se hi test kar sakte hain ya Python script se.

**Remix se Test karne ka tarika:**
1.  `Deployed Contracts` mein apna contract expand karein.
2.  `sendEth` function dikhega.
3.  Upar **Value** field mein `0.01` likhein aur unit mein `Ether` select karein.
4.  `_receiver` field mein kisi bhi dusre wallet ka address dalein.
5.  `transact` button dabayein. 
6.  **Result:** Aapke MetaMask se 0.01 ETH katega aur receiver ke wallet mein turant pahunch jayega!

---

### **Step 4: Python se Connect Karein**

Jab contract deploy ho jaye, toh uska address apne `.env` file mein update karein:

```env
CONTRACT_ADDRESS=0xAapka_Deployed_Contract_Address
```

Aur [worker.py](file:///Users/arbazkudekar/Downloads/python_script/worker.py) ko run karein. Woh automatically is contract ko call karke transactions handle karega.

---

### **Key Concepts (Hinglish)**
- **Payable:** Is keyword ka matlab hai ki yeh function paise (ETH) handle kar sakta hai.
- **msg.value:** Yeh woh amount hai jo aap transaction bhejte waqt saath mein bhej rahe hain.
- **_receiver.transfer:** Yeh command contract ke paas aaye hue paise ko turant receiver ke paas bhej deti hai.

Maine yeh guide **[10_SIMPLE_CONTRACT_TEST.md](file:///Users/arbazkudekar/Downloads/python_script/documentation/10_SIMPLE_CONTRACT_TEST.md)** mein save kar di hai.
