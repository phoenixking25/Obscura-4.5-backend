import os
from flask import Blueprint, request, jsonify
from models import Player, Level, DeclarativeBase
import config as config
from controller import DatabaseHandler
import json
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from gauth import validate_token, tokenGenerate, decoder
import jwt


obscura = Blueprint('obscura', __name__)
database_handler = DatabaseHandler()
session = database_handler.connect_to_database()


def authenticate(email):
    print email
    user = Player.query.filter(Player.idToken == email).first()
    return user

def identity(payload):
    email = payload['email']
    return Player.query.filter(Player.email == email).first()


@obscura.route('/protected', methods = ['GET','POST'])
@jwt_required()
def protected():
    return '%s' % current_identity


@obscura.route('/decode', methods = ['GET', 'POST'])
def tokenDecode():    
    token = request.headers['auth']
    ans = jwt.decode(token, 'secret', algorithms=['HS256'])        
    return ans


@obscura.route('/initial', methods=['GET'])
def initial():
    from controller import DatabaseHandler
    database_handler = DatabaseHandler()
    session = database_handler.connect_to_database()
    session.close()
    return 'ok', 200


@obscura.route('/health', methods=['GET'])
def health(): 
    return {"status":"ok"}, 200

@obscura.route('/player', methods = ['GET'])
def getPlayer():    
        info = Player.query.all()
        x = []
        print info
        for player in info:
            data = {"username":player.username, "level":player.level, "college":player.college}
            x.append(data)
        print x
        return x, 200

@obscura.route('/signup', methods = ['GET', 'POST','PUT'])
def signup():
    if request.method == 'POST':
        info = Player(request.data['name'], request.data['email'], request.data['username'], request.data['college'], request.data['phone'], request.data['level'], request.data['levelId'], request.data['picture'])
        session.add(info)
        session.commit()
        return {"status":"created"}, 201
    return {"status":"enter Player details"}

@obscura.route('/level', methods = ['GET', 'POST'])
def getLevel():
    info = decoder()
    print info
    email = info['email']
    player = Player.query.filter(Player.email == email).first()
    playerLevel = player.level
    level = Level.query.filter(Level.levelNo == playerLevel).first()
    levelAlias = level.name
    return {'alias': levelAlias}, 200

@obscura.route('/getToken', methods = ['POST','GET'])
def getToken():
    if request.method == 'POST':
        token = request.data['token']
        provider = request.data['provider']
        info = validate_token(token, provider)
        user = Player.query.filter(Player.email == info['email']).first()
        if user:
            if info['email'] == user.email:
                jwtToken = tokenGenerate(info['email'], provider)
                return {'backend':info['email'], 'token':jwtToken, 'status':'success'}
        else:
            return {'backend':info['email'], 'status':'failure', 'name':info['name'], 'picture':info['picture'],  }
    return {'error':'token not recieved'}

@obscura.route('/crreateLevel', methods = ['POST', 'GET'])
def createLevel():
    if request.method == 'POST':
        info = Level(request.data['name'], request.data['level'], request.data['nextUrl'], request.data['picture'], request.data['html'], request.data['js'], request.data['hint'], request.data['ans'])
        session.add(info)
        session.commit()
        return {'status':'created'}, 201
    return {'status':'enter level details'}, 200
