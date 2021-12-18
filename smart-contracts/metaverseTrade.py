import smartpy as sp


class MetaverseTrade(sp.Contract):
    """Implements a contract where users can trade one token for another token.

    """

    TRADE_TYPE = sp.TRecord(
        # Flag to indicate if the trade has been exectuded
        executed=sp.TBool,
        # Flag to indicate if the trade has been cancelled
        cancelled=sp.TBool,
        # The time when the trade proposal was submitted
        timestamp=sp.TTimestamp,
        # The wallet that initially proposed the trade
        issuer=sp.TAddress,
        # The token id that the issuer is offering
        token=sp.TNat,
        # The token id that the issuer wants
        for_token=sp.TNat).layout(
            ("executed", ("cancelled", ("timestamp", ("issuer", ("token", "for_token"))))))

    def __init__(self, metadata, fa2, expiration_time=sp.nat(5)):
        """Initializes the contract.

        """
        # Define the contract storage data types for clarity
        self.init_type(sp.TRecord(
            metadata=sp.TBigMap(sp.TString, sp.TBytes),
            fa2=sp.TAddress,
            expiration_time=sp.TNat,
            trades=sp.TBigMap(sp.TNat, MetaverseTrade.TRADE_TYPE),
            counter=sp.TNat))

        # Initialize the contract storage
        self.init(
            metadata=metadata,
            fa2=fa2,
            expiration_time=expiration_time,
            trades=sp.big_map(),
            counter=0)

    def check_no_tez_transfer(self):
        """Checks that no tez were transferred in the operation.

        """
        sp.verify(sp.amount == sp.tez(0),
                  message="The operation does not need tez transfers")

    def check_trade_still_open(self, trade_id):
        """Checks that the trade id corresponds to an existing trade and that
        the trade is still open (not executed and not cancelled).

        """
        # Check that the trade id is present in the trades big map
        sp.verify(self.data.trades.contains(trade_id),
                  message="The trade id doesn't exist")

        # Check that the trade was not executed
        trade = self.data.trades[trade_id]
        sp.verify(~trade.executed, message="The trade was executed")

        # Check that the trade was not cancelled
        sp.verify(~trade.cancelled, message="The trade was cancelled")

    @sp.entry_point
    def propose_trade(self, trade_proposal):
        """Proposes a trade.

        """
        # Define the input parameter data type
        sp.set_type(trade_proposal, sp.TRecord(
            token=sp.TNat,
            for_token=sp.TNat).layout(("token", "for_token")))

        # Check that no tez have been transferred
        self.check_no_tez_transfer()

        # Transfer the proposed token to the barter account
        self.fa2_transfer(
            fa2=self.data.fa2,
            from_=sp.sender,
            to_=sp.self_address,
            token_id=trade_proposal.token,
            token_amount=1)

        # Update the trades bigmap with the new trade information
        self.data.trades[self.data.counter] = sp.record(
            executed=False,
            cancelled=False,
            timestamp=sp.now,
            issuer=sp.sender,
            token=trade_proposal.token,
            for_token=trade_proposal.for_token)

        # Increase the trades counter
        self.data.counter += 1

    @sp.entry_point
    def accept_trade(self, trade_id):
        """Accepts and executes a trade.

        """
        # Define the input parameter data type
        sp.set_type(trade_id, sp.TNat)

        # Check that the trade is still open
        self.check_trade_still_open(trade_id)

        # Check that no tez have been transferred
        self.check_no_tez_transfer()

        # Check that the trade has not expired
        has_expired = sp.now > self.data.trades[trade_id].timestamp.add_minutes(
            sp.to_int(self.data.expiration_time))
        sp.verify(~has_expired, message="The trade has expired")

        # Set the trade as executed
        trade = self.data.trades[trade_id]
        trade.executed = True

        # Transfer the sender token to the issuer
        self.fa2_transfer(
            fa2=self.data.fa2,
            from_=sp.sender,
            to_=trade.issuer,
            token_id=trade.for_token,
            token_amount=1)

        # Transfer the issuer token to the sender
        self.fa2_transfer(
            fa2=self.data.fa2,
            from_=sp.self_address,
            to_=sp.sender,
            token_id=trade.token,
            token_amount=1)

    @sp.entry_point
    def cancel_trade(self, trade_id):
        """Cancels a proposed trade.

        """
        # Define the input parameter data type
        sp.set_type(trade_id, sp.TNat)

        # Check that the trade is still open
        self.check_trade_still_open(trade_id)

        # Check that no tez have been transferred
        self.check_no_tez_transfer()

        # Check that the sender is the trade issuer
        trade = self.data.trades[trade_id]
        sp.verify(sp.sender == trade.issuer,
                  message="Only the issuer can cancel the trade")

        # Set the trade as cancelled
        trade.cancelled = True

        # Transfer the token back to the sender
        self.fa2_transfer(
            fa2=self.data.fa2,
            from_=sp.self_address,
            to_=sp.sender,
            token_id=trade.token,
            token_amount=1)

    def fa2_transfer(self, fa2, from_, to_, token_id, token_amount):
        """Transfers a number of editions of a FA2 token between two addresses.

        """
        # Get a handle to the FA2 token transfer entry point
        c = sp.contract(
            t=sp.TList(sp.TRecord(
                from_=sp.TAddress,
                txs=sp.TList(sp.TRecord(
                    to_=sp.TAddress,
                    token_id=sp.TNat,
                    amount=sp.TNat).layout(("to_", ("token_id", "amount")))))),
            address=fa2,
            entry_point="transfer").open_some()

        # Transfer the FA2 token editions to the new address
        sp.transfer(
            arg=sp.list([sp.record(
                from_=from_,
                txs=sp.list([sp.record(
                    to_=to_,
                    token_id=token_id,
                    amount=token_amount)]))]),
            amount=sp.mutez(0),
            destination=c)


# Add a compilation target
sp.add_compilation_target("metaverseTrade", MetaverseTrade(
        metadata=sp.utils.metadata_of_url("ipfs://Qmc9P5ouY3QGhMzPwWKUnBxPAXo8o3AKjBgFxJYAh7zhzA"),
        fa2=sp.address("KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv"),
        expiration_time=sp.nat(5)))
