import sys
from Node import Node

def start_node():
    # argv[0] is always the program itself on the command line
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    key_file = None

    if len(sys.argv) > 4:
        key_file = sys.argv[4]

    node = Node(ip, port, key_file)
    node.start_p2p()
    node.start_API(api_port)

if __name__ == '__main__':
    start_node()