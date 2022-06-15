import threading, time
from Message import Message
from utils import BlockchainUtils

class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socket_communication = node

    def start(self):
        status_thread = threading.Thread(target=self.status, args=())
        status_thread.start()
        
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    def status(self):
        while True:
            print('status')
            time.sleep(10)

    def discovery(self):
        while True:
            print('discovery...')
            time.sleep(10)

    def handshake(self, node):
        handshake_message = self.handshake_message()
        self.socket_communication.send(node, handshake_message)

    def handshake_message(self):
        own_connector = self.socket_communication.socket_connector
        own_peers = self.socket_communication.peers
        data = own_peers
        message_type = 'DISCOVERY'
        message = Message(own_connector, message_type, data)

        encoded_message = BlockchainUtils.encode(message)
        return encoded_message
