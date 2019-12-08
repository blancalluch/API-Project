import requests
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from mongoAtlasConnection import coll_sent, db_sent
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
import bson
from bson.json_util import dumps
from bottle import route, run, get, post, request
from mongoAtlasConnection import coll, db
#from api_get import chatSentiment


def CollectionInfo():
    '''devuelve un diccionario con el usuario y un string con todos sus mensajes'''
    query = list(coll_sent.find())
    idusers = coll_sent.distinct("idUser")
    users = set([q["idUser"] for q in query])
    user_message = {}
    for u in users:
        user_message[f'{u}'] = ""
    for q in query:
        user_message[str(q["idUser"])] += " "+q["Message"]
    return {"user_message": user_message, "userId's": idusers}


@get("/user/<user_id>/recommend")
def recommendingUsers(user_id):
    '''devuelve una lista con los 3 usuarios que más se parecen all usuario insertado'''
    user_message = CollectionInfo()
    if int(user_id) not in user_message["userId's"]:
        return f"{user_id}'s' sentiments aren't analyzed."
    else:
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        i = 0
        for m in user_message["user_message"].values():
            tokenizer = RegexpTokenizer(r"\w+")
            tokens = tokenizer.tokenize(m)
            clean_text = [ct for ct in tokens if ct not in stop_words]
            user_message[str(i)] = " ".join(clean_text)
            i += 1
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(
            user_message["user_message"].values())
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix,
                          columns=count_vectorizer.get_feature_names(),
                          index=user_message["user_message"].keys())
        similarity_matrix = distance(df, df)
        sim_df = pd.DataFrame(
            similarity_matrix, columns=user_message["user_message"].keys(), index=user_message["user_message"].keys())
        np.fill_diagonal(sim_df.values, 0)

        return dumps(zip(list(sim_df[user_id].sort_values(ascending=False)[:].index),
                         list(sim_df[user_id].sort_values(ascending=False)[:])))
