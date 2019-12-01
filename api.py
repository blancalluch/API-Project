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
    print(f"Chat")
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

@post("/user/create")
def creatUser():
    n=max(coll.distinct("idUser"))+1
    names=(coll.distinct("userName"))
    name=request.forms.get("userName")
    if name in names:
        return "Name alreasy exists"
    else:
        info={"userName":name,
            "idUser":n}
        coll.insert_one(info)
        return f"User_id: {n}"





'''
@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}

def newUser():
    name = str(request.forms.get("name"))
    new_id = max(coll.distinct("idUser")) + 1
    new_user = {
        "idUser": new_id,
        "userName": name
    }
    collection.insert_one(new_user)

@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}
'''

db, coll = mon.connectCollection('chats','chats')
mon.add_json(1,coll)
run(host='0.0.0.0', port=8080)