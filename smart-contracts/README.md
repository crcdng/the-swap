# Smart contracts

This directory contrains all the smart contracts used in the project.


## SmartPy installation

```bash
wget https://smartpy.io/cli/install.sh
bash ./install.sh local-install ~/admin/smartpy
rm install.sh
```

## Execute the tests

```bash
cd ~/the-swap/smart-contracts
~/admin/smartpy/SmartPy.sh test metaverseTrade_test.py output/tests/metaverseTrade --html --purge
```

## Compile the contract

```bash
cd ~/the-swap/smart-contracts
~/admin/smartpy/SmartPy.sh compile metaverseTrade.py output/contract/metaverseTrade --html --purge
```

## Try them in the hangzhou2net

| Contract | Address | | |
| ---------| ------- | --- | --- |
| Metaverse trade | KT1LZR4wt2Ws27jKqmhviQxLgJfSkve94VwX | [TzKT](https://hangzhou2net.tzkt.io/KT1LZR4wt2Ws27jKqmhviQxLgJfSkve94VwX/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/KT1LZR4wt2Ws27jKqmhviQxLgJfSkve94VwX/operations) |
| FA2 token | KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv | [TzKT](https://hangzhou2net.tzkt.io/KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv/operations) |
| crcdng faucet 1 | tz1XtK77MM5vFHskWaSQ8mmgvTgHjZLW74sR | [TzKT](https://hangzhou2net.tzkt.io/tz1XtK77MM5vFHskWaSQ8mmgvTgHjZLW74sR/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/tz1XtK77MM5vFHskWaSQ8mmgvTgHjZLW74sR/operations) |
| crcdng faucet 2 | tz1hsws5poquGgQsFpEiMyMDjrUvxJHALwjs | [TzKT](https://hangzhou2net.tzkt.io/tz1hsws5poquGgQsFpEiMyMDjrUvxJHALwjs/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/tz1hsws5poquGgQsFpEiMyMDjrUvxJHALwjs/operations) |
| jagracar faucet | tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN | [TzKT](https://hangzhou2net.tzkt.io/tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN/operations) |
