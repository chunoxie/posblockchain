from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler

class SocketCommunication(Node):
    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery_handler = PeerDiscoveryHandler(self)

    def start_socket_communication(self):
        self.start()
        self.peer_discovery_handler.start()

    def inbound_node_connected(self, node):
        #return super().inbound_node_connected(node)
        print(f"Inbound connection <<<\nfrom {node} ")
        self.send_to_node(node, ' <<< Hi, I am the node you connected to...')

    def outbound_node_connected(self, node):
        #return super().outbound_node_connected(node)
        print(f"Outbound connection >>>\nto {node} ")
        self.send_to_node(node, '>>> Hi, I am the node who initialized the connection...')

    def node_message(self, node, data):
        #return super().node_message(node, data)
        print(data)