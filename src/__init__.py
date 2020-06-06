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
