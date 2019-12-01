from bottle import route, run, get, post, request
import random
import mongoAtlasConnection as mon
import bson
from bson.json_util import dumps

@get("/")
def index():
    return dumps(coll.find())

@get("/usernames")
def usernames():
    return dumps(coll.find({},{"userName":1}))

@get("/chats")
def chats():
    return dumps(coll.find({},{"idChat":1}))

@get("/chat/<chat_id>")
def oneChat(chat_id):
    return dumps(coll.find({"idChat":int(chat_id)}))

def existing(element):
    data=index()
    c=[]
    for d in range(len(data)):
        c.append((data[d][element]))
    return set(c)

@post("/username/<name>")
def creatName(name):
    print(f"Información de: {name}")
    n=existing(name)
    if dumps(coll.find({"userName":name}))==[]:
        coll.insert_one()
    return dumps(coll.find({"userName":name}))


'''
@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}
'''

db, coll = mon.connectCollection('chats','chats')
run(host='0.0.0.0', port=8080)