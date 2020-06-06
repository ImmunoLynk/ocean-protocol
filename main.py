import flask
from flask_cors import CORS

from src.account import _get_account

from ocean_utils.agreements.service_types import ServiceTypes
from mantaray_utilities.events import subscribe_event
from ocean_keeper.web3_provider import Web3Provider
from ocean_keeper import Keeper
from squid_py import (
    Ocean,
    Config
)

from src import default_config_dict, metadata

FLASK_APPLICATION_NAME = 'ocean-protocol'
TRANSACTION_RULE = '/transaction'

config_dict = default_config_dict # ? use this dict? Do we want to input more configurations? If so, how and why?

configuration = Config(config_dict=config_dict)
squid_py.ConfigProvider.set_config(configuration)

app = flask.Flask(FLASK_APPLICATION_NAME)
CORS(app)

ocn = Ocean(configuration)
keeper = Keeper.get_instance()

MARKET_PLACE_PROVIDER_ADDRESS = Web3Provider.get_web3().toChecksumAddress(configuration.provider_address)


@app.route(TRANSACTION_RULE, methods=['POST'])
def process_transaction():
    """Route for making a transaction between seller and buyer

    Request JSON:
        {
            "publisher": {
                "address": <address point>,
                "private_key": <private key>
            },
            "consumer": {
                "address": <address point>,
                "private_key": <private key>
            },
            "price": <float representing price>
        }
    """

    # initialize return dict
    data = {"success": False}

    if flask.request.method == "POST":

        # get file containing all information needed for transaction happen
        _file = flask.request.files.get('transaction')
        if _file:
            publisher_acct = _get_account(_file.get("publisher"))
            consumer_acct = _get_account(_file.get("consumer"))

            # update the price
            metadata.update({
                "price": float(_file.get("price"))
            })

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

            # update request status

            data.update({
                "success": True
            })

    return flask.jsonify(data)

if __name__ == "__main__":
    app.run()