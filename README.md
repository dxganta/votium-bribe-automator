# Automatic Gauge Votes Incentives On Votium
## Summary
### [BribesManager.sol](https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/BribesManager.sol)
The main contract is the BribesManager.sol contract. It has no admin controls.

On deployment of the contract, the user needs to input the following parameters:
 1. <strong>token</strong>: The contract address of the reward/incentive (ERC20 Token) that will be used for bribing.
 2. <strong>gaugeIndex</strong>: The index of the gauge in the voting proposal.
 3. <strong>tokensPerVote</strong>: The amount of tokens that will be sent to the votium bribing contract per voting proposal.

 Anybody can send tokens to the contract to be used for bribing.
 Once sent the user has to call the <strong>sendBribe()</strong> method to send the tokens to the votium bribing contract. <strong>The sendBribe()</strong> method requires a single parameter <strong>_proposal (bytes32</strong>) which is the snapshot IPFS has id of the ongoing proposal. If the hash id of some other proposal is used other than the ongoing one, the transaction will revert.

 The <strong>sendBribe()</strong> method can be called only once per voting proposal. If called more than once for the same proposal then the method will revert with the message <strong>"Bribe already sent"</strong>. 

 The <strong>sendBribe()</strong> method will also revert if the contract doesn't have any tokens for bribing.

 If the contract has more than zero tokens but less than TOKEN_PER_VOTE tokens, then the <strong>sendBribe()</strong> method will send whatever tokens the contract has to the votium bribe contract.

 ### [BribesLogic.sol](https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/library/BribesLogic.sol)
 This is a library which contains all the logic for the BribesManager contract. This needs to by deployed just once.

 ### [BribesFactory.sol](https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/BribesFactory.sol)
This is a factory contract added for ease of deployment of the BribesManager contract by any user. This also reduces the gas cost for deploying a BribesManager contract (details below under Gas Costs section). This Factory contract needs to be deployed just once.

The user has to call the <strong>deployManager()</strong> method with the required parameters to deploy a new BribesManager contract. A <strong>NewManager</strong> event is emitted on contract deployment to keep logs of all the managers deployed.
## Installation & Setup

1. Install [Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) & [Ganache-CLI](https://www.npmjs.com/package/ganache-cli), if you haven't already.

2. Copy the .env.example file, and rename it to .env

3. Sign up for Alchemy and generate an API key. Store it in the ALCHEMY_KEY environment variable.

4. Sign up for Etherscan and generate an API key. This is required for fetching source codes of the ethereum mainnet contracts we will be interacting with. Store the API key in the ETHERSCAN_TOKEN environment variable.

Install the dependencies in the package
```
## Python Dependencies
pip install -r requirements.txt
```

## Tests
 Tests for all the mentioned specifications for the contract are included in the [tests/test_main.py](https://github.com/realdiganta/crv-bribe-automator/blob/main/tests/test_main.py) file. We are running the tests in a forked Ethereum Mainnet starting at block 13767837, to test on the Gauge Weight Vote Proposal for the week of 9th Dec, 2021. To run the tests run the following command
```
brownie test
```
<img src="https://user-images.githubusercontent.com/47485188/146224068-8c27bb71-ce1c-4eff-9458-8ef8be34d8cf.png"> </img>

## Gas Costs
At first, I created a single BribesManager contract with all the code in it. But the deployment cost was very high. So I changed it to a library-contract architecture where the <strong>[BribesLogic](https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/library/BribesLogic.sol)</strong> library contains all the logic and the <strong>[BribesManager](https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/BribesManager.sol)</strong> stores the state variables. This reduced the cost of deploying the BribesManager to 199252 gas.
I further added another <strong>[BribesFactory]((https://github.com/realdiganta/votium-bribe-automator/blob/main/contracts/BribesFactory.sol)) </strong>contract which can be used to deploy new BribesManager using the deployManager() method. This further reduces the gas cost of deploying a BribesManager contract to <strong>190566 gas</strong>.
<img src="https://user-images.githubusercontent.com/47485188/146815191-e265f02e-4846-4483-9e97-77c11007b10a.png"> </img>

## Deployed Addresses (Ropsten Testnet)
1. BribesLogic Library : [0xBE2B68865D63893929a70ddaD63D1596F4F02518](https://ropsten.etherscan.io/address/0xBE2B68865D63893929a70ddaD63D1596F4F02518)
2. BribesFactory Contract : [0x3Bf391aCF28a315eB83aD90270e3517Bfc131C7F](https://ropsten.etherscan.io/address/0x3bf391acf28a315eb83ad90270e3517bfc131c7f)
3. BribesManager Contract : [0xD2340282f3289B3d6c80A697C42A11E820dEA5B0](https://ropsten.etherscan.io/address/0xD2340282f3289B3d6c80A697C42A11E820dEA5B0)

## Notes
Importance has been given here on reducing gas costs as compared to accessiblity. For example, in the BribesManager contract you may see that I have made the storage variables private (TOKEN, GAUGE_INDEX, TOKENS_PER_VOTE). This was done to reduce gas costs. One might ask that when sending bribes a user might want to know about the token address, gauge_index, tokens per vote etc. of the BribesManager contract. But as you can see on contract deployment of the BribesManager using the deployManager() method in the BribesFactory contract, an NewManager() event is emitted. So for the UI we can easily get the details of any BribesManager contract by querying that event.


For any queries please ping me on discord diganta.eth#0692 or mail at digantakalita.ai@gmail.com