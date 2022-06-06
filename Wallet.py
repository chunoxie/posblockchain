from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Transaction import Transaction
from utils import BlockchainUtils

class Wallet:
    def __init__(self):
        self.key_pair = RSA.generate(2048)

    def sign(self, data):
        data_hash = BlockchainUtils.hash(data)
        signature_scheme_object = PKCS1_v1_5.new(self.key_pair)
        signature = signature_scheme_object.sign(data_hash)
        return signature.hex()

    @staticmethod
    def signature_valid(data, signature, public_key_string):
        signature = bytes.fromhex(signature)
        data_hash = BlockchainUtils.hash(data)
        public_key = RSA.importKey(public_key_string)
        signature_scheme_object = PKCS1_v1_5.new(public_key)
        signature_valid = signature_scheme_object.verify(data_hash, signature)
        return signature_valid

    def public_key_string(self):
        public_key_string = self.key_pair.publickey().exportKey('PEM').decode('utf-8')
        return public_key_string

    def create_transaction(self, receiver_public_key, amount, type):
        transaction = Transaction(self.public_key_string(), receiver_public_key, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction