# ocean-protocol
Integration to Ocean so users can offer data on the marketplace.

## Ethereum connection
Web.py is used in order to run a local node and enable transactions over Ocean. Flask-web3 is also employed to integrate incoming metadata with the ethereum network and also so facilitate block navigation and debugging.

### Installation
```bash
pip install flask
pip install flask_web3
cd web3.py
virtualenv venv
. venv/bin/activate
pip install -e .[dev]
```
For further instructions on how it works refer to the [original repo](https://github.com/ethereum/web3.py).