# Local Smart Contract Development Guide (Hinglish)

Agar aap hamesha Remix use nahi karna chahte aur apne computer par locally contracts likhna, test karna aur deploy karna chahte hain, toh yeh guide aapke liye hai. 

Duniya mein do sabse famous tools hain iske liye: **Hardhat** aur **Foundry**. Hum **Hardhat** (JavaScript/TypeScript based) se shuru karenge kyunki yeh beginner-friendly hai.

---

### **1. Environment Setup**

Apne terminal mein yeh commands run karein:

```bash
# Naya folder banayein
mkdir my-blockchain-project
cd my-blockchain-project

# Node.js project initialize karein
npm init -y

# Hardhat install karein
npm install --save-dev hardhat

# Hardhat project setup karein
npx hardhat
# (Select "Create a JavaScript project" and press Enter for all questions)
```

---

### **2. Local Blockchain Run Karein**

Hardhat aapko ek "Local Node" deta hai jo aapke computer par blockchain chalata hai. Iska fayda yeh hai ki yeh **free** hai aur **instant** kaam karta hai.

```bash
npx hardhat node
```
Yeh command aapko 20 test accounts degi jisme har ek mein **10000 ETH** honge (sirf testing ke liye).

---

### **3. Contract Likhein aur Compile Karein**

1.  `contracts/` folder mein apni file rakhein (jaise `SimpleTransfer.sol`).
2.  Compile karne ke liye run karein:
    ```bash
    npx hardhat compile
    ```

---

### **4. Local Testing (Sabse Important)**

Remix mein aap manual test karte hain, lekin local dev mein aap **Test Scripts** likhte hain. `test/` folder mein ek file banayein `Lock.js` ki jagah:

```javascript
const { expect } = require("chai");

describe("SimpleTransfer", function () {
  it("Should transfer funds correctly", async function () {
    const [owner, receiver] = await ethers.getSigners();
    const SimpleTransfer = await ethers.getContractFactory("SimpleTransfer");
    const contract = await SimpleTransfer.deploy();

    await contract.sendEth(receiver.address, { value: ethers.parseEther("1.0") });
    
    // Check if receiver got the money
    const balance = await ethers.provider.getBalance(receiver.address);
    expect(balance).to.equal(ethers.parseEther("10001.0")); // 10000 + 1
  });
});
```

Test run karne ke liye: `npx hardhat test`

---

### **5. Deploy to Sepolia (Locally)**

1.  `hardhat.config.js` mein apni **Private Key** aur **Alchemy URL** dalein.
2.  `scripts/deploy.js` script likhein.
3.  Command run karein:
    ```bash
    npx hardhat run scripts/deploy.js --network sepolia
    ```

---

### **Summary (Remix vs Local)**

| Feature | Remix | Hardhat (Local) |
| :--- | :--- | :--- |
| **Ease of Use** | Very Easy | Medium (Needs Setup) |
| **Testing** | Manual (Slow) | Automated (Fast & Professional) |
| **Project Size** | Small (1-2 files) | Large (Professional Projects) |
| **Version Control** | Hard (No Git) | Easy (Git Support) |

Maine yeh guide **[12_LOCAL_SMART_CONTRACT_DEV.md](file:///Users/arbazkudekar/Downloads/python_script/documentation/12_LOCAL_SMART_CONTRACT_DEV.md)** mein save kar di hai. Professional developers hamesha Hardhat ya Foundry hi use karte hain!
