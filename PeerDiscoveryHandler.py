import threading, time

class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socket_communication = node

    def start(self):
        status_thread = threading.Thread(self.status, args=())
        status_thread.start()
        
        discovery_thread = threading.Thread(self.discovery, args=())
        discovery_thread.start()

    def status(self):
        while True:
            print('status')
            time.sleep(10)

    def discovery(self):
        while True:
            print('discovery...')
            time.sleep(10)