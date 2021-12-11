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
| FA2 token | KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv | [TzKT](https://hangzhou2net.tzkt.io/KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/KT1VQR797ZJJV9PH2onbGjuDBwvNxE9V72Zv/operations) |
| Metaverse trade contract | KT1FgzUUXrWDGjmDW62z22Mq7RUXAe4YjLxU | [TzKT](https://hangzhou2net.tzkt.io/KT1FgzUUXrWDGjmDW62z22Mq7RUXAe4YjLxU/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/KT1FgzUUXrWDGjmDW62z22Mq7RUXAe4YjLxU/operations) |
| jagracar faucet | tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN | [TzKT](https://hangzhou2net.tzkt.io/tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN/operations/) | [better-call.dev](https://better-call.dev/hangzhou2net/tz1gnL9CeM5h5kRzWZztFYLypCNnVQZjndBN/operations) |
