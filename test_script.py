import pprint
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from utils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys
from POS import ProofOfStake
from Lot import Lot

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

    blockchain = Blockchain()
    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    block_count = blockchain.blocks[-1].block_count + 1

    block = wallet.create_block(pool.transactions, last_hash, block_count)

    if not blockchain.last_block_hash_is_valid(block):
        print("\nLast block hash is not valid!\n")

    if not blockchain.block_count_valid(block):
        print("\nBlock count is not valid!\n")

    if blockchain.last_block_hash_is_valid(block) and blockchain.block_count_valid(block):
        blockchain.add_block(block)


    # blockchain.add_block(block)
    print(blockchain.to_json())
    # print("Printing block created from Wallet create_block method:\n", block.to_json())

    # signature_valid = Wallet.signature_valid(block.payload(), block.signature, wallet.public_key_string())
    # print("\nValidating signature:\n", signature_valid)

    # block = Block(pool.transactions, 'last_hash', 'forger', 1)

    # print("\nPrinting list of transactions in the pool\n", pool.transactions)
    # print("\nPrinting a block:\n", block.to_json())

def test_account_model():
    wallet = Wallet()
    account_model = AccountModel()

    #account_model.add_account(wallet.public_key_string())
    account_model.update_balance(wallet.public_key_string(), 10)
    account_model.update_balance(wallet.public_key_string(), -5)
    print(account_model.balances)

def test_covered_transactions():
    blockchain = Blockchain()
    transaction_pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()
    forger = Wallet()

    # Create exchange transaction to fund wallet
    exchange_transaction = exchange.create_transaction(alice.public_key_string(), 10, 'EXCHANGE')

    if not transaction_pool.transaction_exists(exchange_transaction):
        transaction_pool.add_transaction(exchange_transaction)
    covered_transactions = blockchain.get_covered_transaction_set(transaction_pool.transactions)
    
    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    block_count = blockchain.blocks[-1].block_count + 1
    
    #block_one = Block(covered_transactions, last_hash, forger.public_key_string(), block_count)
    block_one = forger.create_block(covered_transactions, last_hash, block_count)
    blockchain.add_block(block_one)

    transaction_pool.remove_from_pool(block_one.transactions)

    # Alice sending 5 to Bob
    transaction = alice.create_transaction(bob.public_key_string(), 5, "TRANSFER")

    if not transaction_pool.transaction_exists(transaction):
        transaction_pool.add_transaction(transaction)
    covered_transactions = blockchain.get_covered_transaction_set(transaction_pool.transactions)

    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    block_count = blockchain.blocks[-1].block_count + 1
    
    #block_two = Block(covered_transactions, last_hash, forger.public_key_string(), block_count)
    block_two = forger.create_block(covered_transactions, last_hash, block_count)
    blockchain.add_block(block_two)

    transaction_pool.remove_from_pool(block_two.transactions)
    
    #print(covered_transactions)
    #pprint.pprint(blockchain.to_json())
    print(blockchain.to_json())

def test_node():
    # argv[0] is always the program itself on the command line
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])

    node = Node(ip, port)
    node.start_p2p()
    node.start_API(api_port)

    # if port == 10002:
    #     node.p2p.connect_with_node('localhost', 10001)

    # print(node.blockchain)
    # print(node.transaction_pool)
    # print(node.wallet)

def test_pos():
    pos = ProofOfStake()
    pos.update('bob', 10)
    pos.update('alice', 100)
    print(pos.get('bob'))
    print(pos.get('alice'))
    print(pos.get('jack'))

def test_lot():
    lot = Lot('bob', 1, 'last_hash')
    print(lot.lot_hash())

if __name__ == '__main__':
    #test_old_transaction()
    #test_new_transaction()
    #test_transaction_pool()
    #test_account_model()
    #test_covered_transactions()
    #test_node()
    #test_pos()
    test_lot()