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

## Try them in hangzhou2net

...
