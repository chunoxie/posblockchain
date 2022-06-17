from flask import Flask, jsonify, request
from flask_classful import FlaskView, route
from utils import BlockchainUtils

node = None

class NodeAPI(FlaskView):
    def __init__(self):
        self.app = Flask(__name__)

    def start(self, api_port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=api_port)

    def inject_node(self, injected_node):
        global node
        node = injected_node

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communication interface to nodes blockchain', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.to_json(), 200

    @route('/transaction_pool', methods=['GET'])
    def transaction_pool(self):
        transactions = {}
        for counter, transaction in enumerate(node.transaction_pool.transactions):
            transactions[counter] = transaction.to_json()
            
        return jsonify(transactions), 200

    @route('transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handle_transaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201