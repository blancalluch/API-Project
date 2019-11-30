from pymongo import MongoClient

def connectCollection(database, collection):
    '''Connecting with mongoDB and reading database collection.'''
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll