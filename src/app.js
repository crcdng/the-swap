import { TezosToolkit } from '@taquito/taquito';
import { BeaconWallet } from '@taquito/beacon-wallet';

export class App {
  constructor(swapContract, rcpClient = 'https://api.tez.ie/rpc/mainnet') {
    this.swapContract = swapContract;
    this.rcpClient = rcpClient;
    this.tk = new TezosToolkit(this.rcpClient);
  }

  init(tokenIdA, tokenIdB) {
    this.setTradeProposal(tokenIdA, tokenIdB);
  }

  setTradeProposal(tokenIdA, tokenIdB) {
    this.tradeProposal = { "token": tokenIdA, "for_token": tokenIdB };
  }

  connectWallet() {
    const options = { name: 'the swap' };
    const wallet = new BeaconWallet(options);

    wallet
      .requestPermissions({ network: { type: 'hangzhounet' } })
      .then((_) => wallet.getPKH())
      .then((address) => { 
        console.log(`Your address: ${address}`);
        if (address != null) { this.address = address };
        } 
      )
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));

    // Tezos.setWalletProvider(wallet);
    this.tk.setWalletProvider(wallet);
    this.wallet = wallet;
  }

  getIpfsMediaLinkFromFromTokenId(haidsh) {
    return 0; // this.tradeId;
  }

  getTradeIdFromOPHash(hash) {
    return 0; // this.tradeId;
  }

  setTradeId(id) {
    this.tradeId = id;
  }

  async initiateSwap(tradeProposal = this.tradeProposal) {
    if (tradeProposal == null) { console.error('ERROR: initiateSwap() - tradeProposal'); return; }
    this.tk.contract
      .at(this.swapContract)
      .then((contract) => {
        return contract.methods.propose_trade(tradeProposal).send();
      })
      .then((op) => {
        console.log(`Waiting for ${op.hash} to be confirmed...`);
        this.tradeId = getTradeIdFromOPHash(hash);
        return op.confirmation(1).then(() => op.hash);
      })
      .then((hash) => console.log(`Operation injected: ${this.rcpClient}/${hash}`))
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));
  }

  async confirmSwap(tradeId = this.tradeId) {
    this.tk.contract
      .at(this.swapContract)
      .then((contract) => {
        if (tradeId == null) { console.error('ERROR: confirmSwap() - tradeId'); return; }
        return contract.methods.accept_trade(tradeId).send();
      })
      .then((op) => {
        console.log(`Waiting for ${op.hash} to be confirmed...`);
        return op.confirmation(1).then(() => op.hash);
      })
      .then((hash) => console.log(`Operation injected: ${this.rcpClient}/${hash}`))
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));
  }

}




