from bottle import route, run, get, post, request
import random
from mongo import CollConection
import bson



@get("/")
def index():
    return {
        "nombre": random.choice(["Pepe", "Juan", "Fran", "Luis"])
    }


@get("/chiste/<tipo>")
def demo2(tipo):
    print(f"un chiste de {tipo}")
    if tipo == "chiquito":
        return {
            "chiste": "Van dos soldados en una moto y no se cae ninguno porque van soldados"
        }
    elif tipo == "eugenio":
        return {
            "chiste": "Saben aquell que diu...."
        }
    else:
        return {
            "chiste": "No puedorrr!!"
        }

@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}


coll=CollConection('chats','chats')
run(host='0.0.0.0', port=8080)