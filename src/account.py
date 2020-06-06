"""Core module for account related operations"""
import os
from web3 import Web3

class Account:
    """Class representing an account."""

    def __init__(self, address, password=None, key_file=None, encrypted_key=None, private_key=None):
        """Hold account address, password and either keyfile path, encrypted key or private key

        Args:
            address (str): The address of this account
            password (str): account's password. This is necessary for decrypting the private key
                to be able to sign transactions locally
            key_file (str): str path to the encrypted private key file
            encrypted_key (str):
            private_key (str):
        """
        assert key_file or encrypted_key or private_key, \
            'Account requires one of `key_file`, `encrypted_key`, or `private_key`.'
        if key_file or encrypted_key:
            assert password, '`password` is required when using `key_file` or `encrypted_key`.'

        if private_key:
            password = None

        self.address = address
        self.password = password
        self._key_file = key_file
        if self._key_file and not encrypted_key:
            with open(self.key_file) as _file:
                encrypted_key = _file.read()
        self._encrypted_key = encrypted_key
        self._private_key = private_key

    @property
    def key_file(self):
        if self._key_file:
            return os.path.expandvars(os.path.expanduser(self._key_file))
        return None

    @property
    def key(self):
        if self._private_key:
            return self._private_key

        return self._encrypted_key

def _get_account(data):
    """Utility function to get publisher account

    Args:
        data (dict): Dict containing user info

    Returns:
        Account class
    """

    adds = data.get("address")
    private_key = data.get("private_key")

    return Account(Web3.toChecksumAddress(adds, None, None, None, private_key))