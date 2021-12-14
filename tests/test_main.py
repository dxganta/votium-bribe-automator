import brownie
from brownie import (
    chain,
    accounts,
    interface,
    Contract,
    BribesFactory,
    BribesLogic
)
from config import (
    GAUGE,
    TOKEN,
    TOKENS_PER_VOTE
)


def test_main():
    rand_user = accounts[5]
    dust = TOKENS_PER_VOTE * 0.4
    token = interface.IERC20(TOKEN)
    bribeV2 = Contract.from_explorer(
        "0x7893bbb46613d7a4FbcC31Dab4C9b823FfeE1026")
    token_whale = accounts.at(
        "0x627dcd9b5518ace082eafa1f40842b9b45fbbd9c", force=True)
    # deploy library
    BribesLogic.deploy({"from": token_whale})

    # deploy factory
    factory = BribesFactory.deploy({'from': token_whale})

    manager_address = factory.deployManager(
        TOKEN, GAUGE, TOKENS_PER_VOTE,  {"from": token_whale}).return_value

    manager = interface.IBribesManager(manager_address)

    # assert that their are no token rewards before sending bribe
    rewards = bribeV2.reward_per_token(GAUGE, TOKEN)
    assert rewards == 0

    # send tokens for bribing
    token.transfer(manager, TOKENS_PER_VOTE * 2 + dust, {'from': token_whale})

    # bribe
    manager.sendBribe({'from': token_whale})

    rewards = bribeV2.reward_per_token(GAUGE, TOKEN)
    assert rewards > 0

    # test that bribes cannot be sent again for the same voting cycle
    with brownie.reverts("Bribe already sent"):
        manager.sendBribe({'from': token_whale})

    # fast-forward 1 week
    chain.sleep(86400 * 7)
    chain.mine()

    # test that now bribing can be done since this is a new week
    # also that sendBribe can be called by any user
    manager.sendBribe({"from": rand_user})

    rewards = bribeV2.reward_per_token(GAUGE, TOKEN)
    assert rewards > 0

    # now after sending bribes 2 times. A token amount greater than 0 but less than TOKENS_PER_VOTE will be left
    # since we initially filled the contract with TOKENS_PER_VOTE*2 + dust tokens
    # so calling the sendBribe() function must send whatever tokens is left to the bribe contract
    chain.sleep(86400 * 7)
    chain.mine()

    balance = token.balanceOf(manager)
    assert balance > 0 and balance < TOKENS_PER_VOTE

    manager.sendBribe({'from': rand_user})

    assert token.balanceOf(manager) == 0

    # now the contract has zero tokens
    # assert that the sendBribe() function reverts when the contract has zero tokens
    chain.sleep(86400 * 7)
    chain.mine()

    with brownie.reverts("No tokens"):
        manager.sendBribe({'from': token_whale})

    # now lets top up the contract  and test that bribe sending works again
    token.transfer(manager, TOKENS_PER_VOTE * 10, {'from': token_whale})

    # also test the votesLeft function
    # assert manager.votesLeft() == 10

    manager.sendBribe({'from': rand_user})
    rewards = bribeV2.reward_per_token(GAUGE, TOKEN)
    assert rewards > 0
