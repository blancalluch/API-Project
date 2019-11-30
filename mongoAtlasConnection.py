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

db, coll = connectCollection('chat_conversations','chat_conversations')

with open('./input/chats.json') as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)