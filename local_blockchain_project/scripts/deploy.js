const hre = require("hardhat");

async function main() {
  const SimpleTransfer = await hre.ethers.getContractFactory("SimpleTransfer");
  const simpleTransfer = await SimpleTransfer.deploy();

  await simpleTransfer.waitForDeployment();

  console.log("SimpleTransfer deployed to:", await simpleTransfer.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
