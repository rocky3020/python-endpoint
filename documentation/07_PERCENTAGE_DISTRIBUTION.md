# Percentage-Based Distribution Guide (Hinglish)

Agar aap chahte hain ki ek hi transaction mein funds alag-alag wallets mein percentage ke hisaab se distribute ho jayein (jaise A: 20%, B: 30%, C: 50%), toh aapko ek **Splitter Smart Contract** ki zarurat hogi.

---

### 1. Smart Contract Code (Solidity)

Aap niche diya gaya code use kar sakte hain. Yeh contract amount lega aur use define kiye gaye addresses par split kar dega.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FundSplitter {
    
    // Function jo funds receive karega aur distribute karega
    function distribute(
        address payable addrA, 
        address payable addrB, 
        address payable addrC
    ) public payable {
        uint256 total = msg.value;
        require(total > 0, "Amount 0 nahi ho sakta");

        // Percentage Calculation (A: 20%, B: 30%, C: 50%)
        uint256 amountA = (total * 20) / 100;
        uint256 amountB = (total * 30) / 100;
        uint256 amountC = total - amountA - amountB; // Bacha hua 50% (Rounding errors se bachne ke liye)

        // Funds Transfer
        addrA.transfer(amountA);
        addrB.transfer(amountB);
        addrC.transfer(amountC);
    }

    // Contract balance check karne ke liye
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
```

---

### 2. Yeh Kaise Kaam Karta Hai? (Hinglish Explanation)

- **Input:** Jab aapka Python server is contract ke `distribute` function ko call karega, toh woh saath mein **ETH (ya native token)** bhejega.
- **Calculation:** Contract apne aap total amount ka 20%, 30%, aur 50% calculate kar lega.
- **Rounding Error Protection:** Maine 50% ko calculate karne ki jagah `total - amountA - amountB` kiya hai. Iska fayda yeh hai ki agar division mein 1-2 wei (sabse choti unit) ka farak aaye, toh contract fail nahi hoga aur saara paisa distribute ho jayega.
- **Push Logic:** Yeh abhi bhi **Push Logic** hai kyunki server transaction trigger kar raha hai aur addresses server hi provide kar raha hai.

---

### 3. Python Server mein kya badlav honge?

Aapko apne Python code mein `contract.functions.distribute(...)` ko call karna hoga.

**Example Python Snippet:**
```python
# Wallets aur Amount define karein
wallets = ["0xAddrA...", "0xAddrB...", "0xAddrC..."]
total_amount_in_wei = w3.to_wei(1, 'ether') # 1 ETH distribute karna hai

# Contract function call karein
tx = contract.functions.distribute(
    wallets[0], 
    wallets[1], 
    wallets[2]
).build_transaction({
    'from': SERVER_ADDRESS,
    'value': total_amount_in_wei, # Yeh amount distribute hoga
    'nonce': w3.eth.get_transaction_count(SERVER_ADDRESS),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})

# Sign aur Send (Wahi purana process)
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
```

---

### 4. Iske Fayde (Benefits)
1. **Ek hi Transaction:** Aapko 3 alag-alag transactions nahi karne padenge. Isse **Gas Fees bachti hai**.
2. **Trustless:** Code guarantees deta hai ki percentage sahi distribute hogi.
3. **Speed:** Teeno wallets mein ek saath paisa pahuch jayega.

Maine is guide ko aapke documentation folder mein **[07_PERCENTAGE_DISTRIBUTION.md](file:///Users/arbazkudekar/Downloads/python_script/documentation/07_PERCENTAGE_DISTRIBUTION.md)** ke naam se save kar diya hai.
