import { TezosToolkit } from '@taquito/taquito';

export class App {
  constructor (rcpClient = 'https://api.tez.ie/rpc/mainnet') {
    this.tk = new TezosToolkit(rcpClient);
  }

  init (address) { this.address = address; }

  async getBalance (address = this.address) {
    let balance = 0.0;
    try {
      const rawBalance = await this.tk.rpc.getBalance(address);
      balance = rawBalance.toNumber() / 1000000;
    } catch (error) {
      console.error("Could not get a balance. Check the address you entered and try again.");
    }
    return balance;
  }
}