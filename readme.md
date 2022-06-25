**To test the file**

Activate virtual environment:
- source env/Scripts/activate (for Windows)
- source env/bin/activate (for Linux)

Start the two instances of peer and API servers. First instance requires key to be the initial forger to add transactions to the blockchain
- python -m backend.app.start localhost 10001 5005 backend/keys/genesisPrivateKey.pem
- python -m backend.app.start localhost 10002 5002

Issue a transaction
- python -m backend.tests.Interaction

Go to the browsers on localhost:5005/blockchain and localhost:5002/blockchain to view the blockchain

Start a third instance to see if the new instance will be updated with the latest blockchain
- python -m backend.app.start localhost 10003 5003

Visit the browser on localhost:5003/blockchain

Simulate a staker
- python -m backend.app.start localhost 10004 5004 backend/keys/stakerPrivateKey.pem

To increase threshold for transactions within a single block before forging, visit backend/transact/TransactionPool.py and set it in forger_required method.