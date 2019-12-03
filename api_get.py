from bottle import route, run, get, post, request
import random
from mongoAtlasConnection import coll, db
from mongoAtlasConnection import coll_sent, db_sent
import bson
from bson.json_util import dumps
import api_post
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from functools import reduce
import recommending


@get("/")
def index():
    '''devuelve toda la informacion de la api'''
    return dumps(coll.find())


@get("/usernames")
def usernames():
    '''devuelve los usernames de la api'''
    return dumps(coll.find({}, {"userName": 1}))


@get("/chats")
def chats():
    '''devuelve los chats de la api'''
    print(f"Chat")
    return dumps(coll.find({}, {"idChat": 1}))


@get("/chat/<chat_id>/list")
def oneChat(chat_id):
    '''devuelve una lista con los mensajes del chat indicado'''
    data = list(coll.find({"idChat": int(chat_id)}, {"_id": 0}))
    return {
        "messages": [[d["idUser"], d["idMessage"], d["text"]] for d in data]
    }


@get("/chat/<chat_id>/sentiment")
def chatSentiment(chat_id):
    '''devuelve una lista de diccionarios con los nombres, mensajes y sentimientos del chat seleccionado'''
    texts = oneChat(chat_id)
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    for d in list(texts['messages']):
        info_m = {}
        info_m["idUser"] = d[0]
        info_m["idMessage"] = d[1]
        info_m["Message"] = d[2]
        info_m["Sentiment"] = sid.polarity_scores(d[2])
        sentiments.append(info_m)
    if coll_sent.find({"idChat": int(chat_id)}) == []:
        coll_sent.insert_many(sentiments)
    comp_sent = [s['Sentiment']['compound'] for s in sentiments]
    avg = reduce((lambda x, y: x+y), comp_sent)/len(comp_sent)
    return dumps({"sentiments": sentiments,
                  "compound sentiments": comp_sent,
                  "avg sentiment [-1,1]": avg})


run(host='0.0.0.0', port=8080)
