from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from utils import BlockchainUtils

class Node:
    def __init__(self, ip, port, key = None):
        self.p2p = None
        self.ip = ip 
        self.port = port 
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.from_key(key)

    def start_p2p(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)

    def start_API(self, api_port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(api_port)

    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key

        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)
        
        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, 'TRANSACTION', transaction)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)

            forging_required = self.transaction_pool.forger_required()
            if forging_required:
                self.forge()

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.public_key_string():
            print('I am the next forger')
            block = self.blockchain.create_block(self.transaction_pool.transactions, self.wallet)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, 'BLOCK', block)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
        else:
            print('I am not the next forger')