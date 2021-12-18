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

  async connectWallet() {
    const options = { name: 'the swap' };
    const wallet = new BeaconWallet(options);
    let address = wallet
      .requestPermissions({ network: { type: 'hangzhounet' } })
      .then((_) => wallet.getPKH())
      .then((address) => {
        if (address != null) {          // note address 0 won't work    
          this.wallet = wallet;
          this.tk.setWalletProvider(wallet);
          return address;
        };
      }
      )
      .catch((error) => console.log(`connectWallet Error: ${JSON.stringify(error, null, 2)}`));
    return address;
  }

  getIpfsMediaLinkFromFromTokenId(id) {
    throw 'Not implemented yet: getIpfsMediaLinkFromFromTokenId';
    // return ""; 
  }

  async getTradeIdFromOPHash(hash) {
    throw 'Not implemented yet: getTradeIdFromOPHash';
    // return 0;
  }

  setTradeId(id) {
    this.tradeId = id;
  }

  async initiateSwap(tradeProposal = this.tradeProposal) {
    console.log("calling propose_trade operation");
    if (tradeProposal == null) { console.error('ERROR: initiateSwap() - tradeProposal'); return; }
    if (this.tk.wallet == null) { console.error('ERROR: initiateSwap() - this.tk.wallet'); return; }

    // console.dir(`WALLLET ${this.tk.wallet}`);

    this.tk.wallet
      .at(this.swapContract)
      .then((contract) => {
        return contract.methods.propose_trade(tradeProposal.token, tradeProposal.for_token).send();
      })
      .then((op) => {
        console.log(`Waiting for ${op.hash} to be confirmed...`);
        // this.tradeId = getTradeIdFromOPHash(hash);
        return op.confirmation(1).then(() => op.hash);
      })
      // .then((hash) => console.log(`Operation injected: ${this.rcpClient}/${hash}`))
      .then((hash) => console.log(`Operation injected:`))
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));
  }

  async confirmSwap(tradeId = this.tradeId) {
    console.log("calling accept_trade operation");
    this.tk.wallet
      .at(this.swapContract)
      .then((contract) => {
        if (tradeId !== 0 && tradeId == null) { console.error('ERROR: confirmSwap() - tradeId'); return; }
        return contract.methods.accept_trade(tradeId).send();
      })
      .then((op) => {
        console.log(`Waiting for ${op.hash} to be confirmed...`);
        return op.confirmation(1).then(() => op.hash);
      })
      .then((hash) => console.log(`Operation injected: ${this.rcpClient}/${hash}`))
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));
  }

  async cancelSwap(tradeId = this.tradeId) {
    console.log("calling cancel_trade operation");
    this.tk.wallet
      .at(this.swapContract)
      .then((contract) => {
        if (tradeId !== 0 && tradeId == null) { console.error('ERROR: cancelSwap() - tradeId'); return; }
        return contract.methods.cancel_trade(tradeId).send();
      })
      .then((op) => {
        console.log(`Waiting for ${op.hash} to be confirmed...`);
        return op.confirmation(1).then(() => op.hash);
      })
      .then((hash) => console.log(`Operation injected: ${this.rcpClient}/${hash}`))
      .catch((error) => console.log(`Error: ${JSON.stringify(error, null, 2)}`));
  }

}




