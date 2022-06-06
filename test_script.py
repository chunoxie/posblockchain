from Transaction import Transaction
from Wallet import Wallet

def test_transaction():
    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    transaction = Transaction(sender, receiver, amount, type)

    wallet = Wallet()
    signature = wallet.sign(transaction.to_json())

    print("\nPrinting dict directly:\n", transaction.__dict__)
    print("\nPrinting the to_json method:\n", transaction.to_json())
    print("\nPrinting signature from Wallet:\n", signature)

    transaction.sign(signature)
    print("\nPrinting signed transaction the to_json method:\n", transaction.to_json())

if __name__ == '__main__':
    test_transaction()