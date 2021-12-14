// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "../interfaces/token/IERC20.sol";
import "./library/BribesLogic.sol";

contract BribesManager {
    address public immutable TOKEN;
    uint public immutable GAUGE_INDEX;
    uint public immutable TOKENS_PER_VOTE;
    bytes32 public lastProposal;
    address constant VOTIUM_BRIBE = 0x19BBC3463Dd8d07f55438014b021Fb457EBD4595;

    /// @param token Address of the reward/incentive token
    /// @param gaugeIndex index of the gauge in the voting proposal choices
    /// @param tokensPerVote number of tokens to add as incentives per vote
    constructor(address token, uint gaugeIndex, uint tokensPerVote) {
        TOKEN = token;
        GAUGE_INDEX = gaugeIndex;
        TOKENS_PER_VOTE = tokensPerVote;
    }

    function sendBribe(bytes32 _proposal) public {
        IERC20(TOKEN).approve(VOTIUM_BRIBE, TOKENS_PER_VOTE);
        BribesLogic.sendBribe(TOKEN, _proposal, TOKENS_PER_VOTE, GAUGE_INDEX, lastProposal, VOTIUM_BRIBE);
        lastProposal = _proposal;
    }
}