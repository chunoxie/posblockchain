from time import time


class Block:
    def __init__(self, transactions, last_hash, forger, block_count):
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.block_count = block_count
        self.timestamp = time()
        self.signature = ''

    def to_json(self):
        data = {}
        data['last_hash'] = self.last_hash
        data['forger'] = self.forger
        data['block_count'] = self.block_count
        data['timestamp'] = self.timestamp

        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.to_json())
            
        data['transactions'] = json_transactions
        return data