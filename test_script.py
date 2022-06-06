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

    # transaction.sign(signature)
    print("\nPrinting signed transaction the to_json method:\n", transaction.to_json())

    signature_valid = Wallet.signature_valid(transaction.to_json(), signature, wallet.public_key_string())
    print("\nTesting if signature is valid:\n", signature_valid)

if __name__ == '__main__':
    test_transaction()