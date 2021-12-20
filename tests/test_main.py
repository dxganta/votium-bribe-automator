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
    GAUGE_INDEX,
    TOKEN,
    TOKENS_PER_VOTE
)


# constants
PROPOSAL = "0xc26deaa05f45f3f6ad088cb6603d77cb2e826ff98b69e9a122706a37c8694681"


def test_main():
    '''
        There is currently no on-going proposal. 
        So we are testing on the Gauge Weight Vote Proposal for the week of 9th Dec, 2021
        on a forked Ethereum mainnet from block #13767837
    '''
    rand_user = accounts[5]
    token = interface.IERC20(TOKEN)
    token_whale = accounts.at(
        "0x63278bf9acdfc9fa65cfa2940b89a34adfbcb4a1", force=True)
    # deploy library
    BribesLogic.deploy({"from": token_whale})

    # deploy factory
    factory = BribesFactory.deploy({'from': token_whale})

    tx = factory.deployManager(
        TOKEN, GAUGE_INDEX, TOKENS_PER_VOTE,  {"from": token_whale})

    manager_address = tx.return_value

    # assert that the NewManager event was emitted successfully
    event = tx.events["NewManager"][0][0]

    assert event['bribesManager'] == manager_address
    assert event['token'] == TOKEN
    assert event['gaugeIndex'] == GAUGE_INDEX
    assert event['tokensPerVote'] == TOKENS_PER_VOTE

    manager = interface.IBribesManager(manager_address)

    # test that the sendBribe function fails when the manager contract has zero tokens
    with brownie.reverts("No tokens"):
        manager.sendBribe(PROPOSAL, {'from': token_whale})

    # fill the manager contract with tokens for bribing
    token.transfer(manager, TOKENS_PER_VOTE * 5, {'from': token_whale})

    # assert that bribes cannot be sent for a random or old proposal
    # the contract must sent the bribe only for the current ongoing proposal
    with brownie.reverts("Proposal Expired"):
        old_proposal = "0x0c0550515f038293f31eb10dc002881d1f7f5c170bca3e9a23eec7900d499bf7"
        manager.sendBribe(old_proposal, {'from': token_whale})

    # send bribes for the current ongoing proposal
    # also sending the transaction from a random user to test that anybody can call the sendBribe function
    tx = manager.sendBribe(PROPOSAL, {'from': rand_user})

    # the Bribed Event is emitted by the Votium Bribe contract
    event = tx.events['Bribed'][0][0]

    # assert that the votiumBribe contract received the bribes successfully
    assert event['_token'] == TOKEN
    assert event['_choiceIndex'] == GAUGE_INDEX
    assert event['_proposal'] == PROPOSAL
    # The votium bribe contract keeps 4% of the bribe sent as fees so actual amount will be (tokens_per_vote - 4%)
    assert event['_amount'] == TOKENS_PER_VOTE - (0.04 * TOKENS_PER_VOTE)

    # test that bribes cannot be sent again for the same voting proposal
    with brownie.reverts("Bribe already sent"):
        manager.sendBribe(PROPOSAL, {'from': token_whale})
