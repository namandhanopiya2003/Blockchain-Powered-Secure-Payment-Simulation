import os
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class EncryptionManager:
    def __init__(self):
        # List of available encryption types
        self.algorithms = ['fernet', 'aes']
        # Starts with the first algorithm
        self.current = 0
        # Generates the encryption keys
        self._gen_keys()

    # Creates a new key and object
    def _gen_keys(self):
        self.fernet_key = Fernet.generate_key()
        self.fernet = Fernet(self.fernet_key)
        # Creates a random AES key and IV
        self.aes_key = os.urandom(16)
        self.aes_iv = os.urandom(16)

    def switch_algorithm(self):
        # Switchs to the next algorithm
        self.current = (self.current + 1) % len(self.algorithms)
        # Generates new keys
        self._gen_keys()
        # Returns the name of the current algorithm
        return self.current_algorithm()

    # Returns the name of the current encryption algorithm
    def current_algorithm(self):
        return self.algorithms[self.current]

    # Gets the current algorithm
    def encrypt(self, plaintext: bytes):
        algo = self.current_algorithm()
        if algo == 'fernet':
            # Uses Fernet to encrypt the plaintext
            token = self.fernet.encrypt(plaintext)
            return {'algo': 'fernet', 'payload': token.hex()}
        else:
            # Use AES to encrypt the plaintext
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_iv)
            ct = cipher.encrypt(pad(plaintext, AES.block_size))
            return {'algo': 'aes', 'iv': self.aes_iv.hex(), 'payload': ct.hex()}

