import sys
from Node import Node

def start_node():
    # argv[0] is always the program itself on the command line
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])

    node = Node(ip, port)
    node.start_p2p()
    node.start_API(api_port)

if __name__ == '__main__':
    start_node()