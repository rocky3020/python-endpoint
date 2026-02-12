const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleTransfer", function () {
  it("Should transfer funds to the receiver", async function () {
    const [owner, receiver] = await ethers.getSigners();

    const SimpleTransfer = await ethers.getContractFactory("SimpleTransfer");
    const simpleTransfer = await SimpleTransfer.deploy();

    const amount = ethers.parseEther("1.0");

    // Initial balance of receiver
    const initialBalance = await ethers.provider.getBalance(receiver.address);

    // Perform transfer through contract
    await simpleTransfer.sendEth(receiver.address, { value: amount });

    // Final balance of receiver
    const finalBalance = await ethers.provider.getBalance(receiver.address);

    // Check if receiver balance increased by 1 ETH
    expect(finalBalance).to.equal(initialBalance + amount);
  });
});
