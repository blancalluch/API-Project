from bottle import route, run, get, post, request
import random
import mongoAtlasConnection as mon
import bson
from bson.json_util import dumps
import datetime


db, coll = mon.connectCollection('chat_conversations','chat_conversations')
url='./input/chats.json'
mon.add_json(1,coll,url)
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

@get("/chat/<chat_id>/list")
def oneChat(chat_id):
    data=list(coll.find({"idChat":int(chat_id)},{"_id":0}))
    print(data)
    return {
        "messages":[d["text"] for d in data]
    }

@post("/user/create")
def creatUser():
    n=max(coll.distinct("idUser"))+1
    names=(coll.distinct("userName"))
    name=request.forms.get("userName")
    if name in names:
        return "Name already exists"
    else:
        info={"userName":name,
            "idUser":n}
        coll.insert_one(info)
        return f"User_id: {n}"

@post("/chat/create")
def creatChat():
    c=max(coll.distinct("idChat"))+1
    users_list=list(request.forms.getall("user_id"))
    info=[]
    for u in users_list:
        user={}
        user_info=(coll.find({"idUser":int(u)},{"userName":1}))
        user["idUser"]=int(u)
        user['userName']=user_info[0]["userName"]
        user['idChat']=c
        info.append(user)
    coll.insert_many(info)
    return f"Chat_id: {c}"

@post("/chat/<chat_id>/adduser")
def addUsertoChat(chat_id):
    res="ok"
    user=request.forms.get("user_id")
    print(user)
    user_info=list(coll.find({"idUser":int(user)},{"userName":1,"idChat":1,"_id":0}))
    print(user_info)
    for u in user_info:
        if u["idChat"]==int(chat_id):
            res= f"User {user} already in chat {chat_id}"
    if res=="ok":   
        info={
            "idUser":int(user),
            "userName":user_info[0]["userName"],
            "idChat": int(chat_id)
            }
        coll.insert_one(info)
        return f"Chat_id: {chat_id}"
    else:
        return res







@post("/chat/<chat_id>/addmessage")
def addMessagetoChat(chat_id):
    res="ok"
    user=request.forms.get("user_id")
    chat=request.forms.get("chat_id")
    text=request.forms.get("text")
    print(user)
    user_info=list(coll.find({"idUser":int(user)},{"userName":1,"idChat":1,"_id":0}))
    print(user_info)
    message_id=max(coll.distinct("idMessage"))+1
    for u in user_info:
        if u["idChat"]==int(chat_id):
            res= f"User {user} already in chat {chat_id}"
    if res=="ok":   
        info={
            "idUser":int(user),
            "userName":user_info[0]["userName"],
            "idChat": int(chat),
            "idMessage":message_id,
            "datetime": datetime.datetime.utcnow(),
            "text": text
            }
        coll.insert_one(info)
        return f"Chat_id: {chat_id}"
    else:
        return res






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

run(host='0.0.0.0', port=8080)