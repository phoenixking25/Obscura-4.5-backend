from flask import Blueprint, request
from models import Player, Level
from controller import DatabaseHandler
from gauth import validate_token, tokenGenerate, decoder

obscura = Blueprint('obscura', __name__)
database_handler = DatabaseHandler()
session = database_handler.connect_to_database()


@obscura.route('/initial', methods=['GET'])
def initial():
    from controller import DatabaseHandler
    database_handler = DatabaseHandler()
    session = database_handler.connect_to_database()
    session.close()
    return 'ok', 200


@obscura.route('/player/', methods = ['GET'])
def leaderboard():   
    if request.headers['auth']:             
        info = Player.query.all()
        if info:
            array = []
            print info
            for player in info:
                data = {"username":player.username, "level":player.levelId, "college":player.college}
                array.append(data)
            return array, 200
        return {'status': 'No Player has joined'}, 403
    else:
        return {'status': 'invalid access'}, 404

@obscura.route('/signup', methods = ['GET', 'POST','PUT'])
def signup():
    if request.method == 'POST':
        info = Player(request.data['name'], request.data['email'], request.data['username'], request.data['college'], request.data['phone'], request.data['level'], request.data['levelId'], request.data['picture'])
        session.add(info)
        session.commit()
        jwt = tokenGenerate(request.data['email'])
        return {'status': 'created', 'token': jwt}, 201
    return {"status":"enter Player details"}


@obscura.route('/level/', methods = ['GET', 'POST'])
def getAlias():
    info = decoder()
    user = Player.query.filter(Player.email == info['email']).first()
    level = Level.query.filter(Level.levelNo == user.levelId).first()
    if not level:
        return {'status':'Level not found'}, 404
    if user.levelId >= level.levelNo:
        return {'alias': level.name}, 200
    else:
        return {'status': 'Not Accessible for the player'}

@obscura.route('/getLevel/<alias>', methods = ['GET', 'POST'])
def getLevel(alias):
    info  = decoder()
    user = Player.query.filter(Player.email == info['email']).first()   
    level = Level.query.filter(Level.name == alias).first()
    if user.levelId >= level.levelNo:
        if level:
            return {'name': level.name, 'picture':level.picture, 'hint':level.hint, 'js':level.js, 'html':level.html}, 200
        else:
            return {'status': 'Level Not Found'}, 404
    else:
        return {'status': 'Player not allowed'}, 403


@obscura.route('/getAns/<alias>', methods = ['GET', 'POST'])
def getAns(alias):
    if request.method == 'POST':
        info = decoder()
        user = Player.query.filter(Player.email == info['email']).first()   
        level = Level.query.filter(Level.name == alias).first()
        if user.levelId == level.levelNo:
            ans = request.data['ans']
            level = Level.query.filter(Level.name == alias).first()
            if level.ans == ans:
                print "Saving"
                Player.save()
                session.query(Player).filter(Player.email == info['email']).update({'levelId': user.levelId + 1})
                session.commit()
                print "Saved"
                nextlevel = Level.query.filter(Level.levelNo == level.levelNo + 1)
                return {'status': 'success', 'nextalias': nextlevel.name}, 200
            else:
                return {'status': 'failure'}, 200
        elif user.levelId > level.levelNo:
            ans = request.data['ans']
            if level.ans == ans:
                nextlevel = Level.query.filter(Level.levelNo == level.levelNo + 1)
                return {'status': 'success', 'nextalias': nextlevel.name}, 200
            else:
                return {'status': 'failure'}, 404
        else:
            return {'status': 'not accessible'}, 404
    return {'status': 'post the ans'}, 200
            

@obscura.route('/getToken/', methods = ['POST','GET'])
def getToken():
    if request.method == 'POST':
        token = request.data['token']
        provider = request.data['provider']
        info = validate_token(token, provider)
        user = Player.query.filter(Player.email == info['email']).first()
        if user:
            if info['email'] == user.email:
                jwt = tokenGenerate(info['email'])
                return {'backend':info['email'], 'token':jwt, 'status':'success'}
        else:
            return {'backend':info['email'], 'status':'failure', 'name':info['name'], 'picture':info['picture'],  }
    return {'error':'token not recieved'}

@obscura.route('/crreateLevel/', methods = ['POST', 'GET', 'PATCH'])
def createLevel():
    if request.method == 'POST':
        info = Level(request.data['name'], request.data['levelNo'], request.data['nextUrl'], request.data['picture'], request.data['html'], request.data['js'], request.data['hint'], request.data['ans'])
        session.add(info)
        session.commit()
        return {'status':'created'}, 201
    return {'status':'enter level details'}, 200
