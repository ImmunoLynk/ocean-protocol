from flask import Flask, jsonify, request
from flask_web3 import current_web3, FlaskWeb3
from web3 import Web3
import json
import settings


# Declare Flask application
app = Flask(__name__)
app.config.update({'ETHEREUM_PROVIDER': 'http', 'ETHEREUM_ENDPOINT_URI': settings.ETHEREUM_ENDPOINT_URI})

# Declare a custom Web3 class
class CustomWeb3(Web3):
    def customBlockNumber(self):
        return self.eth.blockNumber

# Associate a custom FlaskWeb3 extension
class CustomFlaskWeb3(FlaskWeb3):
    web3_class = CustomWeb3

# Declare customized web3 extension
web3 = CustomFlaskWeb3(app=app)
# isinstance(web3, CustomWeb3)

# Declare route
@app.route('/customBlockNumber')
def last_odd_block_number():
    return jsonify({'data': current_web3.customBlockNumber()})

ganache_url = settings.GANACHE_URL
infura_url = "https://mainnet.infura.io/v3/" + settings.INFURA_API_KEY
if settings.ENDPOINT == 'infura':
    web3 = Web3(Web3.HTTPProvider(infura_url))
else:
    web3 = Web3(Web3.HTTPProvider(ganache_url))

# print(web3.isConnected())
# print(web3.eth.blockNumber)

# Fill in your account here
@app.route('/balance')
def get_balance():
    balance = web3.eth.getBalance(settings.ETHEREUM_ACCOUNT)
    return (web3.fromWei(balance, "ether"))

@app.route('/contract')
def get_contract():
    input_json = request.get_json()
    # OMG Address
    abi = input_json.get('address')
    # OMG ABI
    address = input_json.get('abi')

    contract = web3.eth.contract(address=address, abi=abi)

    totalSupply = contract.functions.totalSupply().call()
    print(web3.fromWei(totalSupply, 'ether'))
    print(contract.functions.name().call())
    print(contract.functions.symbol().call())
    balance = contract.functions.balanceOf(settings.ETHEREUM_ACCOUNT).call()
    print(web3.fromWei(balance, 'ether'))
    return balance


@app.route('/transact')
def transact():
    input_json = request.get_json()
    account_1 = input_json.get('acc1')
    account_2 = input_json.get('acc2')
    private_key = input_json.get('key')

    nonce = web3.eth.getTransactionCount(account_1)

    tx = {
        'nonce': nonce,
        'to': account_2,
        'value': web3.toWei(1, 'ether'),
        'gas': settings.GAS,
        'gasPrice': web3.toWei('50', 'gwei'),
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)

    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return web3.toHex(tx_hash)