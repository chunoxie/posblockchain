from Transaction import Transaction

def test_transaction():
    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    transaction = Transaction(sender, receiver, amount, type)
    print("Printing dict directly: ", transaction.__dict__)
    print("Printing the to_json method: ", transaction.to_json())

if __name__ == '__main__':
    test_transaction()