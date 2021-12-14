// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "../interfaces/token/IERC20.sol";
import "./library/BribesLogic.sol";

contract BribesManager {
    address public immutable TOKEN;
    address public immutable GAUGE;
    uint public immutable TOKENS_PER_VOTE;
    uint public lastPeriod;
    address constant CURVE_BRIBE = 0x7893bbb46613d7a4FbcC31Dab4C9b823FfeE1026;

    /// @param token Address of the reward/incentive token
    /// @param gauge address of the curve gauge
    /// @param tokens_per_vote number of tokens to add as incentives per vote
    constructor(address token, address gauge, uint tokens_per_vote) {
        TOKEN = token;
        GAUGE = gauge;
        TOKENS_PER_VOTE = tokens_per_vote;
    }

    function sendBribe() public {
        IERC20(TOKEN).approve(CURVE_BRIBE, TOKENS_PER_VOTE);
        lastPeriod = BribesLogic.sendBribe(TOKEN, GAUGE, TOKENS_PER_VOTE, lastPeriod, CURVE_BRIBE);
    }
}