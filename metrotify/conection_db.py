import pymongo
URI="mongodb://metrotifydb:fw4MRwLQ4hoXONg5@ac-znymkzd-shard-00-00.ysigne7.mongodb.net:27017,ac-znymkzd-shard-00-01.ysigne7.mongodb.net:27017,ac-znymkzd-shard-00-02.ysigne7.mongodb.net:27017/?ssl=true&replicaSet=atlas-14cc8j-shard-0&authSource=admin&retryWrites=true&w=majority&appName=metrotify"

# Connect to a MongoDB Atlas cluster (replace with your credentials)
client = pymongo.MongoClient("URI")

# Access a specific database
db = client["metrotify"]