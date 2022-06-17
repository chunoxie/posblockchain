from Wallet import Wallet
from utils import BlockchainUtils
import requests

def test_interaction():
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