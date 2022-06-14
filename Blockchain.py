from Block import Block
from utils import BlockchainUtils
from AccountModel import AccountModel

class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()

    def add_block(self, block):
        self.blocks.append(block)

    def to_json(self):
        data = {}
        json_blocks = []

        for block in self.blocks:
            json_blocks.append(block.to_json())

        data['blocks'] = json_blocks
        return data

    def block_count_valid(self, block):
        if self.blocks[-1].block_count == block.block_count - 1:
            return True
        else:
            return False

    def last_block_hash_is_valid(self, block):
        latest_blockchain_block_hash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        if latest_blockchain_block_hash == block.last_hash:
            return True
        else:
            return False

    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                print("Transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction):
        if transaction.type == 'EXCHANGE':
            return True
            
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        else:
            return False