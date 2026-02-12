// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleTransfer {
    // Event to log transfers
    event FundsSent(address indexed receiver, uint256 amount);

    // Function to send funds to a specific address
    // 'payable' allows the function to receive ETH
    function sendEth(address payable _receiver) public payable {
        require(msg.value > 0, "Amount must be greater than 0");
        
        // Transfer the ETH sent to this function directly to the receiver
        _receiver.transfer(msg.value);
        
        // Emit event for tracking
        emit FundsSent(_receiver, msg.value);
    }

    // Function to check contract balance (should be 0 as it transfers immediately)
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
