# ErayBD

# importing the libraries
import datetime # each block will have its own timestamp (created, mined...)
import hashlib  # hash the blocks
import json     # convert to blocks to readable format for postman
import requests
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request # flask: web app, jsonify: return messages to postman

# in SHA-256 encoding system, it only accept encoded strings. So, the hashes has to be string.

# part 1 - building a blockchain

class Blockchain:
    
    def __init__(self): # type of constructor on java
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set() # The items in a set list are unordered, so it will appear in random order.
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,     # every block has each number by starting 1
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        
        self.chain.append(block)    # the block that we just created, added to the chain
        self.transactions = [] # once we added the transactions to the block, we must empty the list
        return block    # we returned it to see on postman
    
    def get_previous_block(self):    # returns the last block of the chain
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):    # the rule-setter
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # the rule we set
            
            # our condition is (new_proof**2 - previous_proof**2). if it is provided, it will be added to the chain.
            
            # hashlib - class
            # sha256 - encoding type
            # sha256's methods - a rule that we have set (new_proof**2 - previous_proof**2)
            # encode - regulates the sha256 encoding as it should be
            # hexdigest - turns the encoded value into a hexdigits which is 64 character long string
            
            if (hash_operation[:4] == '0000'):  # if hash_operation variable's first four digits are 0000
                check_proof = True   # then we got what we want
                
            else:
                new_proof += 1  # if it is not, then try the other proofs
            
        return new_proof   # we returned it to see on postman
        
    def hash(self, block):  # returns the cryptographic hash of the block
        encoded_block = json.dumps(block, sort_keys = True).encode()     # json.dumps - takes an object and makes it a string
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]   # we starting to control if it is valid from block number one
        block_index = 1
        
        while (block_index < len(chain)):
            block = chain[block_index] # we just initialize the block as current block
            
            if (block['previous_hash'] != self.hash(previous_block)):
                # this if statement checks that: if the previous hash of our current block...
                # is different than the hash of it's previous block
                
                # we're using self.hash here 'cause hash is a method of the class Blockchain,
                # not a seperate class. So, self means 'in this class'
                
                return False
            
            previous_proof = previous_block['proof']    # proof of our previous block
            proof = block['proof']  # proof of our current block
            
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if (hash_operation[:4] != '0000'):
                return False
            
            previous_block = block  # previous_block updated to our current block for the loop
            block_index += 1  # block_index updated for the loop
            # end of while loop
            
        return True     # if everything went well (confirmed that the chain is valid) then we return True
                
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1  # returns the next block's number which will be created
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc) # we only want the netloc address (ip and port) (ex. 127.0.0.1:5000)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None # None keyword is used to define a null value, or no value at all.
        max_length = len(self.chain)
        
        for node in network:    # loop in the network's nodes
            response = requests.get(f'http://{node}/get_chain') # f-string type formatted, 'node's are URLs
            
            if response.status_code == 200: # if everything is OK
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_length and self.is_chain_valid(chain):  # if current chain is the largest
                    max_length = length
                    longest_chain = chain
                    
        if longest_chain: # if longest_chain is None, that means the chain has been replaced
            self.chain = longest_chain
            return True # if the chain is not the longest one, the chain needs to be replaced
        return False  # if the chain is the longest one, that is if does need to be replaced
            
        

# part 2 - mining our blockchain

# creating a web app
app = Flask(__name__)

# creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')
    
# creating a blockchain
blockchain = Blockchain()   # a blockchain object from Blockchain class
    
# mining a new block
@app.route("/mine_block", methods=['GET'])
def mine_block():   # mining a block
    previous_block = blockchain.get_previous_block()    
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Eray', amount = 1)
    
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)    # a new block mined with the all infos
    
    response = {'message': 'Congrulations, you just mined a block!',        # left side is dictionary of block
                'index': block['index'],                                    # right side is the info we got
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    # response is a dictionary
    
    return jsonify(response), 200 # 200 means OK on HTTP Status Codes

@app.route("/get_chain", methods=['GET'])   
def get_chain():    # write down the blockchain list with the all infos
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

# checking if the blockchain is valid
@app.route("/is_valid", methods=['GET'])
def is_valid():     
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if (is_valid):
        response = {'message': 'All good. The Blockchain is valid.'}
        return jsonify(response), 200
    
    else:
        response = {'message': 'Something is wrong. The Blockchain is not valid.'}
        return jsonify(response), 406   # 406 means NOT ACCEPTABLE on HTTP Status Codes
        
# adding a new transaction to the blockchain
@app.route("/add_transaction", methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction is missing.', 400 # 400 -> Bad Request
    
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}.'}
    
    return jsonify(response), 200


# part 3 - decentralizing our blockchain

# connecting new nodes
@app.route("/connect_node", methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if nodes is None:
        return "No node", 400
    
    for node in nodes:
        blockchain.add_node(node)
        
    response = {'message': 'All the nodes are now connected. The ErayBD-Coin Blockchain now contains the following  nodes:',
                'total nodes': list(blockchain.nodes)}
    
    return jsonify(response), 201

# replacing the chain by the longest chain if needed
@app.route("/replace_chain", methods=['GET'])
def replace_chain():     
    is_chain_replaced = blockchain.replace_chain()
    # True, if chain needs to be replaced
    # False, if chain doesn't need to be replaced
    
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    
    else:
        response = {'message': 'All good. The chain is the largest one. it does not have to be replaced.',
                    'actual_chain': blockchain.chain}
        
    return jsonify(response), 200 # 200 means OK on HTTP Status Codes

# running the app
app.run(host = '0.0.0.0', port = 5001)