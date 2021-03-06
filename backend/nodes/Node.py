from backend.transact.TransactionPool import TransactionPool
from backend.transact.Wallet import Wallet
from backend.transact.Blockchain import Blockchain
from backend.nodes.SocketCommunication import SocketCommunication
from backend.nodes.NodeAPI import NodeAPI
from backend.nodes.Message import Message
from backend.utils.utils import BlockchainUtils
import copy

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

    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_is_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)

        if not block_count_valid:
            #print('I am requesting for blockchain.')
            self.request_chain()

        if last_block_hash_valid and forger_valid and transactions_valid and signature_valid:
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)

            message = Message(self.p2p.socket_connector, 'BLOCK', block)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)

    def request_chain(self):
        message = Message(self.p2p.socket_connector, 'BLOCKCHAINREQUEST', None)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)
        print('I am requesting for blockchain.')

    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socket_connector, 'BLOCKCHAIN', self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_blockchain_block_count = len(blockchain.blocks)

        if local_block_count < received_blockchain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
                    
            self.blockchain = local_blockchain_copy

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