from brownie import (
    accounts,
    interface,
    BribesManager,
    BribesLogic,
    BribesFactory
)
from config import (
    GAUGE,
    TOKEN,
    TOKENS_PER_VOTE
)


def test_gas_costs():
    token_whale = accounts.at(
        "0x627dcd9b5518ace082eafa1f40842b9b45fbbd9c", force=True)
    dust = TOKENS_PER_VOTE * 0.4
    token = interface.IERC20(TOKEN)

    # deply the BribesLogic library first
    BribesLogic.deploy({"from": token_whale})

    # this will show the gas costs of directly deploying the BribesManager contract
    manager = BribesManager.deploy(
        TOKEN, GAUGE, TOKENS_PER_VOTE,  {"from": token_whale})

    # send tokens for bribing
    token.transfer(manager, TOKENS_PER_VOTE * 2 + dust, {'from': token_whale})

    # bribe
    manager.sendBribe()

    # factory
    factory = BribesFactory.deploy({"from": token_whale})
    # this will show the gas cost of deploying the BribesManager contract using the factory contract
    manager_f = factory.deployManager(
        TOKEN, GAUGE, TOKENS_PER_VOTE, {"from": token_whale})
