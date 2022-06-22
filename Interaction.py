from Block import Block
from Wallet import Wallet
from utils import BlockchainUtils
import requests

def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver.public_key_string(), amount, type)
    url = 'http://localhost:5005/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)

def test_interaction():
    bob = Wallet()
    alice = Wallet()
    alice.from_key('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    # forger: genesis
    post_transaction(exchange, alice, 100, 'EXCHANGE')
    post_transaction(exchange, bob, 100, 'EXCHANGE')
    post_transaction(alice, alice, 25, 'STAKE')

    # forger: most likely Alice
    post_transaction(alice, bob, 1, 'TRANSFER')


if __name__ == '__main__':
    test_interaction()