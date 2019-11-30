#!/usr/bin/python3

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import pandas as pd
import json

import clear

DATABASE_URL = os.environ['DATABASE_URL']
#Connect to DB
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#creates a new database session and returns a new connection instance

#If permission Error
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

#Create Cursor
cur = conn.cursor()

#Create Tables
query = """
CREATE TABLE IF NOT EXISTS users (
  idUser INT NOT NULL, 
  userName VARCHAR(45) NOT NULL,
  PRIMARY KEY (idUser));
CREATE TABLE IF NOT EXISTS chats (
  idChat INT NOT NULL,
  PRIMARY KEY (idChat));
CREATE TABLE IF NOT EXISTS messages (
  idMessage INT NOT NULL,
  text VARCHAR(120) NULL,
  datetime VARCHAR(45) NULL,
  users_idUser INT NOT NULL,
  chats_idChat INT NOT NULL,
  PRIMARY KEY (idMessage),
    FOREIGN KEY (users_idUser)
    REFERENCES users (idUser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Message_chats1
    FOREIGN KEY (chats_idChat)
    REFERENCES chats (idChat)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)"""


cur.execute(query)
#execute database commands and queries
print("Database created.")

#Populate Tables

query = "INSERT INTO {} VALUES {} RETURNING {}"


with open('my-application/input/chats.json') as f:
    chats_json = json.load(f)


users = list(set([(chats_json[i]['idUser'],chats_json[i]['userName']) for i in range(len(chats_json))]))

chats = list(set([(chats_json[i]['idChat']) for i in range(len(chats_json))]))

for user in users:
  q = query.format('users (idUser, userName)',"({}, '{}')".format(user[0],user[1]),'users.idUser')
  print(q)
  try:
    cur.execute(q)
    #send commands to the database

    #Get Response
    id = cur.fetchone()[0]
    #retrieving data from the database

    print(f"value inserted: {id}")
  except:
    print("At least I tried")

for chat in chats:
  q = query.format('chats(idChat)',"({})".format(chat),'chats.idChat')
  print(q)
  try:
    cur.execute(q)
    #send commands to the database

    #Get Response
    id = cur.fetchone()[0]
    #retrieving data from the database

    print(f"value inserted: {id}")
  except:
    print("At least I tried")

for message in chats_json:
  q = query.format('messages(idMessage, text, datetime, users_idUser, chats_idChat)',"({},'{}','{}',{},{})".format(message['idMessage'],message['text'],message['datetime'],message['idUser'],message['idChat'],),'messages.idMessage')
  print(q)
  try:
    cur.execute(q)
    #send commands to the database

    #Get Response
    id = cur.fetchone()[0]
    #retrieving data from the database
    
    print(f"value inserted: {id}")
  except:
    print("At least I tried")
    
print('Done!')