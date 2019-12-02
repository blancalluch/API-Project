#!/usr/bin/python3

from pymongo import MongoClient
import getpass
import json
import os
from dotenv import load_dotenv
load_dotenv()

#Get Password
connection = os.getenv("MONGODB_CONNECT")

#Connect to DB
client = MongoClient(connection)
def connectCollection(database, collection):
    '''Connecting with mongoDB and reading database collection.'''
    db = client[database]
    coll = db[collection]
    return db, coll

#url='./input/chats.json'
def add_json(rem,coll,url):
    with open(url) as f:
        chats_json = json.load(f)
    if rem:    
        coll.remove({})
    coll.insert_many(chats_json)