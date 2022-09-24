# cryptocurrency-demo
Creating our cryptocurrency on our blockchain from scratch.  

``
Note: This is the upgraded version of 'blockchain-demo' repo. Cryptocurrency transactions were combined with the blockchain network.
``                                     

[Click here](https://github.com/ErayBD/blockchain-demo/) to check out 'blockchain-demo' repo.

## Requirements for the demo:
* Python3 - Programming language
* Flask - Web framework for Python
* Postman - API

## Introducting

* Through Flask, we run each nodes (on 5001, 5002 and 5003 ports) that we created from the original file.

![1](https://user-images.githubusercontent.com/71061070/192102601-057d587c-1f95-427a-92c7-c2977b5cc203.jpg)

* While the server is running, let's go to the postman application and test our methods.
```
/mine_blocks
```
```
/get_chain
```
```
/is_valid
```
```
/add_transaction
```
```
/connect_node
```
```
/replace_chain
```

## /get_chain - Shows all the blocks in the chain with all the infos it contains.

![4](https://user-images.githubusercontent.com/71061070/192103485-d321983e-214f-43c1-8c1b-eb5cbad3c464.jpg)

## /mine_block - Adds a new block to the chain with all the infos it contains.

### Port 5001
![1](https://user-images.githubusercontent.com/71061070/192103488-8b372dd3-a463-43db-b7fd-2075a2431518.jpg)

### Port 5002
![2](https://user-images.githubusercontent.com/71061070/192103489-e158c29f-92c7-412b-9562-707b8d2d1b30.jpg)

### Port 5003
![3](https://user-images.githubusercontent.com/71061070/192103491-6e12d6a4-2a19-4c04-bb8b-54f36b895ffb.jpg)


## /is_valid - Checks whether the chain is valid.

![5](https://user-images.githubusercontent.com/71061070/192103605-f259d75d-6bfb-4d0e-b97c-33c99269542e.jpg)

## /connect_node - All nodes are connected to each other so they can synced to the longest chain when necessary.

![6](https://user-images.githubusercontent.com/71061070/192103963-aefd3906-a91f-4488-95e0-60a96ba436cf.jpg)

## /add_transaction - A transaction is added to the mempool to be added to the next block created.

![7](https://user-images.githubusercontent.com/71061070/192104163-ac091cb5-2a25-42c0-96e4-bb02d5ca08d1.jpg)

### When a new block is created, it contains the transaction.
![8](https://user-images.githubusercontent.com/71061070/192104281-c112357c-5454-4ac1-aeb8-b97da056c8c6.jpg)

## /replace_chain - Chains are synced to the longest chain at regular intervals.

![9](https://user-images.githubusercontent.com/71061070/192104427-e065a4fd-0cce-4b8a-9df0-b63eadd88b26.jpg)
