import json

from flask import (
    Flask,
    jsonify,
    request
)

from mantaray_utilities.events import subscribe_event
from ocean_keeper import Keeper
from ocean_keeper.web3_provider import Web3Provider
from ocean_utils.agreements.service_types import ServiceTypes
from squid_py import (
    Ocean,
    Config
)

FLASK_APPLICATION_NAME = 'ocean-protocol'
TRANSACTION_RULE = '/transaction'

# ! For some guidance:
# <https://docs.oceanprotocol.com/concepts/introduction/>
# <https://docs.oceanprotocol.com/concepts/pacific-network/#ocean-components-connected-to-pacific>

# TODO: take a look at https://docs.oceanprotocol.com/tutorials/connect-to-networks/
default_config_dict = {
    'keeper-contracts': {
        'keeper.url': 'https://nile.dev-ocean.com',
        'parity.url': 'https://nile.dev-ocean.com',
        'keeper.path': 'artifacts_nile',
        'secret_store.url': 'https://secret-store.nile.dev-ocean.com/',
        'faucet.url': 'https://faucet.nile.dev-ocean.com',
        
        'parity.address': '',
        'parity.password': '',
    },
    'resources': {
        'aquarius.url': 'https://aquarius.marketplace.dev-ocean.com',
        'brizo.url': 'https://brizo.marketplace.dev-ocean.com',
        'provider.address': '0x4aaab179035dc57b35e2ce066919048686f82972',

        'storage.path': 'squid_py.db',
        'downloads.path': 'downloads_nile',
    }
}
config_dict = default_config_dict # ? use this dict? Do we want to input more configurations? If so, how and why?

configuration = Config(config_dict=config_dict)
squid_py.ConfigProvider.set_config(configuration)

app = Flask(FLASK_APPLICATION_NAME)
ocn = Ocean(configuration) # TODO: define configuration
keeper = Keeper.get_instance()

MARKET_PLACE_PROVIDER_ADDRESS = Web3Provider.get_web3().toChecksumAddress(configuration.provider_address)


def _process_error(
    e,
    error_file='error.json'
):
    message = f'Error message: {e}'
    with open(error_file, 'w') as err:
        json.dump(message, err)
    return jsonify({'status' : message})


@app.route(TRANSACTION_RULE, methods=['POST'])
def process_transaction():
    try:
        publisher_acct = _get_publisher_account() # TODO: implement function
        consumer_acct = _get_consumer_account() # TODO: implement function
        
        # TODO: define metadata
        
        ddo = ocn.assets.create(metadata, publisher_acct, providers=[MARKET_PLACE_PROVIDER_ADDRESS])
        agreement_id = ocn.assets.order(
            ddo.did,
            ddo.get_service(ServiceTypes.ASSET_ACCESS).index,
            consumer_acct,
            provider_address=MARKET_PLACE_PROVIDER_ADDRESS
        )
        subscribe_event("created agreement", keeper, agreement_id)
        subscribe_event("lock reward", keeper, agreement_id)
        subscribe_event("access secret store", keeper, agreement_id)
        subscribe_event("escrow reward", keeper, agreement_id)
        
        ocn.assets.consume(
            agreement_id,
            ddo.did,
            'Access',
            consumer_acct,
            'downloads_nile'
        )
        
    except Exception as e:
        return _process_error(e)