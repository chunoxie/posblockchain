from backend.transact.Wallet import Wallet
from backend.utils.utils import BlockchainUtils
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
    alice.from_key('backend/keys/stakerPrivateKey.pem')
    exchange = Wallet()

    # # forger: genesis
    # post_transaction(exchange, alice, 100, 'EXCHANGE')
    # post_transaction(exchange, bob, 100, 'EXCHANGE')
    # post_transaction(exchange, alice, 25, 'STAKE')

    # # forger: most likely Alice
    # post_transaction(alice, bob, 1, 'TRANSFER')

    # forger: genesis
    post_transaction(exchange, alice, 1000, 'EXCHANGE')
    post_transaction(exchange, bob, 100, 'EXCHANGE')
    post_transaction(exchange, bob, 10, 'EXCHANGE')

    # forger: most likely Alice
    post_transaction(exchange, alice, 25, 'STAKE')
    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')

def old_transaction():
    bob = Wallet()
    alice = Wallet()
    exchange = Wallet()

    transaction = exchange.create_transaction(alice.public_key_string(), 10, 'EXCHANGE')
    url = 'http://localhost:5005/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)


if __name__ == '__main__':
    test_interaction()
    # old_transaction()