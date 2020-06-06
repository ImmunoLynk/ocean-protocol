"""Core module for account related operations"""
import os

from web3 import Web3
from ocean_keeper.account import Account as OceanAccount

def get_account(
    data: dict
):
    """Utility function to get publisher or consumer account.

    Args:
        data (dict): Dict containing user info

    Returns:
        Account class
    """

    address = data.get('address')
    private_key = data.get('private_key')

    return OceanAccount(
        Web3.toChecksumAddress(address),
        None,
        None,
        None,
        private_key
    )