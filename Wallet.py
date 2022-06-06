from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from utils import BlockchainUtils

class Wallet:
    def __init__(self):
        self.key_pair = RSA.generate(2048)

    def sign(self, data):
        data_hash = BlockchainUtils.hash(data)
        signature_scheme_object = PKCS1_v1_5.new(self.key_pair)
        signature = signature_scheme_object.sign(data_hash)
        return signature.hex()