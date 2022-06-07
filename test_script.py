import pprint
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool

def test_old_transaction():
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

    signature_valid = Wallet.signature_valid(transaction.payload(), signature, wallet.public_key_string())
    print("\nTesting if signature is valid:\n", signature_valid)

def test_new_transaction():
    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    wallet = Wallet()
    fraudulent_wallet = Wallet()

    transaction = wallet.create_transaction(receiver, amount, type)
    print("\nPrinting with to_json method\n", transaction.to_json())
    print("\nPrinting with payload method\n", transaction.payload())

    signature_valid = Wallet.signature_valid(transaction.payload(), transaction.signature, wallet.public_key_string())
    print("\nPrint is valid signature:\n", signature_valid)

    fraudulent_signature = Wallet.signature_valid(transaction.payload(), transaction.signature, fraudulent_wallet.public_key_string())
    print("\nPrinting is valid signature with fraudulent wallet:\n", fraudulent_signature)

def test_transaction_pool():
    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    wallet = Wallet()
    pool = TransactionPool()

    transaction = wallet.create_transaction(receiver, amount, type)

    if pool.transaction_exists(transaction) == False: 
        pool.add_transaction(transaction)

    block = wallet.create_block(pool.transactions, 'last_hash', 1)

    blockchain = Blockchain()
    blockchain.add_block(block)
    print(blockchain.to_json())
    # print("Printing block created from Wallet create_block method:\n", block.to_json())

    # signature_valid = Wallet.signature_valid(block.payload(), block.signature, wallet.public_key_string())
    # print("\nValidating signature:\n", signature_valid)

    # block = Block(pool.transactions, 'last_hash', 'forger', 1)

    # print("\nPrinting list of transactions in the pool\n", pool.transactions)
    # print("\nPrinting a block:\n", block.to_json())

if __name__ == '__main__':
    #test_old_transaction()
    #test_new_transaction()
    test_transaction_pool()