from p2pnetwork.node import Node
from backend.nodes.PeerDiscoveryHandler import PeerDiscoveryHandler
from backend.nodes.SocketConnector import SocketConnector
from backend.utils.utils import BlockchainUtils
import json

class SocketCommunication(Node):
    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery_handler = PeerDiscoveryHandler(self)
        self.socket_connector = SocketConnector(ip, port)

    def connect_to_first_node(self):
        if self.socket_connector.port != 10001:
            self.connect_with_node('localhost', 10001)

    def start_socket_communication(self, node):
        self.node = node
        self.start()
        self.peer_discovery_handler.start()
        self.connect_to_first_node()

    def inbound_node_connected(self, node):
        self.peer_discovery_handler.handshake(node)

    def outbound_node_connected(self, node):
        self.peer_discovery_handler.handshake(node)

    def node_message(self, node, data):
        message = BlockchainUtils.decode(json.dumps(data))
        if message.message_type == 'DISCOVERY':
            self.peer_discovery_handler.handle_message(message)
        elif message.message_type == 'TRANSACTION':
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == 'BLOCK':
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == 'BLOCKCHAINREQUEST':
            self.node.handle_blockchain_request(node)
        elif message.message_type == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handle_blockchain(blockchain)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)