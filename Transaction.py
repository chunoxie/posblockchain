import uuid
import time

class Transaction:
    def __init__(self, sender_public_key, receiver_public_key, amount, type):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    def to_json(self):
        return self.__dict__
