from mongoAtlasConnection import coll, db
from bottle import route, run, get, post, request
import datetime
from bottle import response
import bson
from bson.json_util import dumps


@post("/user/create")
def creatUser():
    '''crea un username y la inserta en la api'''
    n = max(coll.distinct("idUser"))+1
    names = (coll.distinct("userName"))
    name = request.forms.get("userName")
    if name in names:
        return "Name already exists"
    else:
        info = {"userName": name,
                "idUser": n}
        coll.insert_one(info)
        return f"User_id: {n}"


@post("/chat/create")
def creatChat():
    '''crea un chat con usuarios y lo inserta en la api'''
    c = max(coll.distinct("idChat"))+1
    users_list = list(request.forms.getall("user_id"))
    info = []
    for u in users_list:
        user = {}
        user_info = (coll.find({"idUser": int(u)}, {"userName": 1}))
        user["idUser"] = int(u)
        user['userName'] = user_info[0]["userName"]
        user['idChat'] = c
        info.append(user)
    coll.insert_many(info)
    return f"Chat_id: {c}"


@post("/chat/<chat_id>/adduser")
def addUsertoChat(chat_id):
    '''añade un usuario al chat indicado y lo inserta en la api'''
    res = "ok"
    user = request.forms.get("user_id")
    user_info = list(coll.find({"idUser": int(user)}, {
                     "userName": 1, "idChat": 1, "_id": 0}))
    print(user_info)
    for u in user_info:
        if u["idChat"] == int(chat_id):
            res = f"User {user} already in chat {chat_id}"
    if res == "ok":
        info = {
            "idUser": int(user),
            "userName": user_info[0]["userName"],
            "idChat": int(chat_id)
        }
        coll.insert_one(info)
        return f"Chat_id: {chat_id}"
    else:
        return res


@post("/chat/<chat_id>/addmessage")
def addMessagetoChat(chat_id):
    '''añade un mensaje de un usuario en el chat indicado y lo inserta en la api'''
    chat_id = int(chat_id)
    user = int(request.forms.get("user_id"))
    text = request.forms.get("text")
    user_info = coll.find_one({"idUser": user, "idChat": chat_id}, {
                              "userName": 1, "idChat": 1, "_id": 0})
    message_id = max(coll.distinct("idMessage"))+1

    if user_info and user_info["idChat"] == chat_id:
        info = {
            "idUser": user,
            "userName": user_info[0]["userName"],
            "idChat": chat_id,
            "idMessage": int(message_id),
            "datetime": datetime.datetime.utcnow(),
            "text": text
        }
        coll.insert_one(info)
        return dumps({"Message_id": message_id})
    else:
        response.status = 500
        return dumps({
            "error": "User does not exist in this chat"
        })
