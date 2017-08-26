import json
from httplib2 import Http
from flask import request
import jwt

def validate_token(access_token, provider):
    h = Http()
    if provider == "google":
        uri = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+access_token
        resp, cont = h.request(uri)
        if not resp['status'] == '200':
            return None

        try:
            data = json.loads(cont)
        except TypeError:
            data = json.loads(cont.decode())

        return data


    if provider == "facebook":
        uri = "https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cemail%2Cpicture&format=json&access_token="+access_token
        resp, cont = h.request(uri)
        if not resp['status'] == '200':
            return None

        try:
            data = json.loads(cont)
        except TypeError:
            data = json.loads(cont.decode())

        return data

def tokenGenerate(email):        
    encoded = jwt.encode({'email': email}, 'secret', algorithm='HS256')
    return encoded

def decoder():
    token = request.headers['auth']
    ans = jwt.decode(token, 'secret', algorithms=['HS256'])        
    return ans