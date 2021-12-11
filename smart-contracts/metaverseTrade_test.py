"""Unit tests for the MetaverseTrade class.

"""

import smartpy as sp

# Import the metaverseTrade and fa2Contract modules
metaverseTrade = sp.io.import_script_from_url("file:metaverseTrade.py")
fa2Contract = sp.io.import_script_from_url("file:templates/fa2Contract.py")


def get_test_environment():
    # Create the test accounts
    user1 = sp.test_account("user1")
    user2 = sp.test_account("user2")
    user3 = sp.test_account("user3")
    fa2_admin = sp.test_account("fa2_admin")

    # Initialize the FA2 contract
    fa2 = fa2Contract.FA2(
        config=fa2Contract.FA2_config(),
        admin=fa2_admin.address,
        metadata=sp.utils.metadata_of_url("ipfs://aaa"))

    # Initialize the metaverse trade contract
    tradeContract = metaverseTrade.MetaverseTrade(
        metadata=sp.utils.metadata_of_url("ipfs://bbb"),
        fa2=fa2.address,
        expiration_time=5)

    # Add all the contracts to the test scenario
    scenario = sp.test_scenario()
    scenario += fa2
    scenario += tradeContract

    # Save all the variables in a test environment dictionary
    testEnvironment = {
        "scenario" : scenario,
        "user1" : user1,
        "user2" : user2,
        "user3" : user3,
        "fa2_admin" : fa2_admin,
        "fa2" : fa2,
        "tradeContract" : tradeContract}

    return testEnvironment


@sp.add_test(name="Test trade")
def test_trade():
    # Get the test environment
    testEnvironment = get_test_environment()
    scenario = testEnvironment["scenario"]
    user1 = testEnvironment["user1"]
    user2 = testEnvironment["user2"]
    user3 = testEnvironment["user3"]
    fa2_admin = testEnvironment["fa2_admin"]
    fa2 = testEnvironment["fa2"]
    tradeContract = testEnvironment["tradeContract"]

    # Mint some tokens
    fa2.mint(
        address=user1.address,
        token_id=sp.nat(0),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://ccc")}).run(sender=fa2_admin)
    fa2.mint(
        address=user1.address,
        token_id=sp.nat(1),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://ddd")}).run(sender=fa2_admin)
    fa2.mint(
        address=user2.address,
        token_id=sp.nat(2),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://eee")}).run(sender=fa2_admin)
    fa2.mint(
        address=user3.address,
        token_id=sp.nat(3),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://eee")}).run(sender=fa2_admin)

    # Add the trade contract as operator for the tokens
    scenario += fa2.update_operators(
        [sp.variant("add_operator", fa2.operator_param.make(
            owner=user1.address,
            operator=tradeContract.address,
            token_id=0)),
        sp.variant("add_operator", fa2.operator_param.make(
            owner=user1.address,
            operator=tradeContract.address,
            token_id=1)),
        sp.variant("add_operator", fa2.operator_param.make(
            owner=user1.address,
            operator=tradeContract.address,
            token_id=2))]).run(sender=user1)
    scenario += fa2.update_operators(
        [sp.variant("add_operator", fa2.operator_param.make(
            owner=user2.address,
            operator=tradeContract.address,
            token_id=2))]).run(sender=user2)
    scenario += fa2.update_operators(
        [sp.variant("add_operator", fa2.operator_param.make(
            owner=user3.address,
            operator=tradeContract.address,
            token_id=3))]).run(sender=user3)

    # Check that the FA2 contract ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100)
    scenario.verify(fa2.data.ledger[(user3.address, 3)].balance == 100)

    # Check that user 1 cannot propose a trade with a token it doesn't own
    scenario += tradeContract.propose_trade(
        token=2,
        for_token=3).run(valid=False, sender=user1)

    # User 1 proposes a trade
    scenario += tradeContract.propose_trade(
        token=0,
        for_token=2).run(valid=False, sender=user1, amount=sp.tez(3))
    scenario += tradeContract.propose_trade(
        token=0,
        for_token=2).run(sender=user1)

    # Check that the FA2 contract ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100 - 1)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100)
    scenario.verify(fa2.data.ledger[(user3.address, 3)].balance == 100)
    scenario.verify(fa2.data.ledger[(tradeContract.address, 0)].balance == 1)

    # Check that the third user cannot accept the trade because it doesn't own
    # the requested token
    scenario += tradeContract.accept_trade(0).run(valid=False, sender=user3)

    # The second user accepts the trade
    scenario += tradeContract.accept_trade(0).run(valid=False, sender=user2, amount=sp.tez(3))
    scenario += tradeContract.accept_trade(0).run(sender=user2)

    # Check that the OBJKT ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100 - 1)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user1.address, 2)].balance == 1)
    scenario.verify(fa2.data.ledger[(user2.address, 0)].balance == 1)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100 - 1)
    scenario.verify(fa2.data.ledger[(user3.address, 3)].balance == 100)
    scenario.verify(fa2.data.ledger[(tradeContract.address, 0)].balance == 0)

    # Check that the second user cannot accept twice the trade
    scenario += tradeContract.accept_trade(0).run(valid=False, sender=user2)

    # Check that the first user cannot cancel the trade because it's executed
    scenario += tradeContract.cancel_trade(0).run(valid=False, sender=user1)


@sp.add_test(name="Test cancel trade")
def test_cancel_trade():
    # Get the test environment
    testEnvironment = get_test_environment()
    scenario = testEnvironment["scenario"]
    user1 = testEnvironment["user1"]
    user2 = testEnvironment["user2"]
    fa2_admin = testEnvironment["fa2_admin"]
    fa2 = testEnvironment["fa2"]
    tradeContract = testEnvironment["tradeContract"]

    # Mint some tokens
    fa2.mint(
        address=user1.address,
        token_id=sp.nat(0),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://ccc")}).run(sender=fa2_admin)
    fa2.mint(
        address=user1.address,
        token_id=sp.nat(1),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://ddd")}).run(sender=fa2_admin)
    fa2.mint(
        address=user2.address,
        token_id=sp.nat(2),
        amount=sp.nat(100),
        metadata={"" : sp.utils.bytes_of_string("ipfs://eee")}).run(sender=fa2_admin)

    # Add the trade contract as operator for the tokens
    scenario += fa2.update_operators(
        [sp.variant("add_operator", fa2.operator_param.make(
            owner=user1.address,
            operator=tradeContract.address,
            token_id=0)),
        sp.variant("add_operator", fa2.operator_param.make(
            owner=user1.address,
            operator=tradeContract.address,
            token_id=1))]).run(sender=user1)
    scenario += fa2.update_operators(
        [sp.variant("add_operator", fa2.operator_param.make(
            owner=user2.address,
            operator=tradeContract.address,
            token_id=2))]).run(sender=user2)

    # Check that the FA2 contract ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100)

    # User 1 proposes a trade
    scenario += tradeContract.propose_trade(
        token=0,
        for_token=2).run(sender=user1)

    # Check that the FA2 contract ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100 - 1)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100)
    scenario.verify(fa2.data.ledger[(tradeContract.address, 0)].balance == 1)

    # Check that the second user cannot cancel the trade
    scenario += tradeContract.cancel_trade(0).run(valid=False, sender=user2)

    # User 1 cancels the trade
    scenario += tradeContract.cancel_trade(0).run(valid=False, sender=user1, amount=sp.tez(3))
    scenario += tradeContract.cancel_trade(0).run(sender=user1)

    # Check that the FA2 contract ledger information is correct
    scenario.verify(fa2.data.ledger[(user1.address, 0)].balance == 100)
    scenario.verify(fa2.data.ledger[(user1.address, 1)].balance == 100)
    scenario.verify(fa2.data.ledger[(user2.address, 2)].balance == 100)
    scenario.verify(fa2.data.ledger[(tradeContract.address, 0)].balance == 0)

    # Check that the first user cannot cancel the trade again
    scenario += tradeContract.cancel_trade(0).run(valid=False, sender=user1)
