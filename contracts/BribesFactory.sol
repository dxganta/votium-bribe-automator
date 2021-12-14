// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./BribesManager.sol";

contract BribesFactory {
    
    event NewManager(address bribesManager, address token, address gauge, uint tokens_per_vote);

    function deployManager(address token, address gauge, uint tokens_per_vote) public returns (BribesManager) {
        BribesManager b = new BribesManager(token, gauge, tokens_per_vote); 
        emit NewManager(address(b), token, gauge, tokens_per_vote);
        return b;
    }
}