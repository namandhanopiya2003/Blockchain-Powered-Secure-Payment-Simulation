import os
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class EncryptionManager:
    def __init__(self):
        self.algorithms = ['fernet', 'aes']
        self.current = 0
        self._gen_keys()

    def _gen_keys(self):
        self.fernet_key = Fernet.generate_key()
        self.fernet = Fernet(self.fernet_key)
        self.aes_key = os.urandom(16)
        self.aes_iv = os.urandom(16)

    def switch_algorithm(self):
        self.current = (self.current + 1) % len(self.algorithms)
        self._gen_keys()
        return self.current_algorithm()

    def current_algorithm(self):
        return self.algorithms[self.current]

    def encrypt(self, plaintext: bytes):
        algo = self.current_algorithm()
        if algo == 'fernet':
            token = self.fernet.encrypt(plaintext)
            return {'algo': 'fernet', 'payload': token.hex()}
        else:
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_iv)
            ct = cipher.encrypt(pad(plaintext, AES.block_size))
            return {'algo': 'aes', 'iv': self.aes_iv.hex(), 'payload': ct.hex()}
