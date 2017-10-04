from flask import Blueprint, request
from models import Player, Level
from controller import DatabaseHandler
from helper import validate_token, tokenGenerate, decoder
import time

obscura = Blueprint('obscura', __name__)
database_handler = DatabaseHandler()
session = database_handler.connect_to_database()



@obscura.route('/leaderboard/', methods = ['GET'])
def leaderboard():
    '''
    Provides the player details for the leaderboard in a array
    '''   
    if request.headers['auth']:             
        # info = Player.query.order_by(Player.levelId.desc()).all()
        info = session.query(Player).order_by(Player.levelId.desc()).all()
        session.close()
        if info:
            array = []
            for player in info:
                data = {'username':player.username, 'level':player.levelId, 'college':player.college}
                array.append(data)
            return array, 200
        return {'status': 'No Player has joined'}, 404
    else:
        return {'status': 'invalid access'}, 401

@obscura.route('/signup', methods = ['POST','PUT'])
def signup():
    '''
    Create a new user
    '''
    if request.method == 'POST':
        print request.data['phone']
        info = Player(request.data['name'], request.data['email'], request.data['username'], request.data['college'], request.data['phone'], request.data['level'], request.data['levelId'], request.data['picture'])
        # casea = Player.query.filter(Player.email == request.data['email']).first()
        # caseb = Player.query.filter(Player.username == request.data['username']).first()
        casea = session.query(Player).filter(Player.email == request.data['email']).first()
        caseb = session.query(Player).filter(Player.username == request.data['username']).first()
        if casea:
            return {'status': 'email already exist', 'token': None}, 409
        elif caseb:
            return {'status': 'username already exist', 'token': None}, 409
        else:
            session.add(info)
            session.commit()
            session.close()
            jwt = tokenGenerate(request.data['email'])
            return {'status': 'created', 'token': jwt}, 201
    return {'status':'enter Player details'}


@obscura.route('/level/', methods = ['GET'])
def getAlias():
    '''
    Return the alias of the level that is going to display in url
    '''
    if (1507289400 - time.time() < 0):
        info = decoder()
        if info:
            # user = Player.query.filter(Player.email == info['email']).first()
            # level = Level.query.filter(Level.levelNo == user.levelId).first()
            user = session.query(Player).filter(Player.email == info['email']).first()
            level = session.query(Level).filter(Level.levelNo == user.levelId).first()
            session.close()
            if not level:
                return {'status':'Level not found', 'alias': ''}, 404
            if user.levelId >= level.levelNo:
                return {'status': 'success', 'alias': level.name}, 200
            else:
                return {'status': 'Not Accessible for the player'}, 403
        else:
            return {'status': 'invalid access'}, 401
    else:
        return {'status': 'failure', 'msg': 'Game has not started yet'}, 200
    

@obscura.route('/level/<alias>', methods = ['GET', 'POST'])
def level(alias):
    '''
    get the alias from the url and return the level respectively
    '''
    if request.method == 'GET':
        if (1507289400 - time.time() < 0):
            info  = decoder()
            if info:
                # user = Player.query.filter(Player.email == info['email']).first()   
                # level = Level.query.filter(Level.name == alias).first()
                user = session.query(Player).filter(Player.email == info['email']).first()
                level = session.query(Level).filter(Level.name == alias).first()
                session.close()  
                if user.levelId >= level.levelNo:
                    if level:
                        return {'name': level.name, 'picture':level.picture, 'hint':level.hint, 'js':level.js, 'html':level.html}, 200
                    else:
                        return {'status': 'failure', 'msg': 'Level Not created'}, 404
                else:
                    return {'status': 'Player not allowed'}, 403
            else:
                return {'status': 'invalid access'}, 401
        else:
            return {'status': 'failure', 'msg': 'Game has not started yet'}, 200
    
    if request.method == 'POST':
        info = decoder()
        if info:
            # user = Player.query.filter(Player.email == info['email']).first()
            # level = Level.query.filter(Level.name == alias).first()
            user = session.query(Player).filter(Player.email == info['email']).first()
            level = session.query(Level).filter(Level.name == alias).first()
            if user.levelId == level.levelNo:
                ans = request.data['ans']
                if ans == level.ans:
                    session.query(Player).filter(Player.email == info['email']).update({'levelId': user.levelId + 1})
                    session.commit()
                    session.close()
                    # user = Player.query.filter(Player.email == info['email']).first()
                    user = session.query(Player).filter(Player.email == info['email']).first()
                    nextLevel = user.levelId + 1
                    # level = Level.query.filter(Level.levelNo == nextLevel).first()
                    level = session.query(Level).filter(Level.levelNo == nextLevel).first()
                    session.close()
                    if level:
                        return {'status': 'success', 'nextalias': level.name}, 200
                    else:
                        return {'status': 'failure', 'msg': 'Level Not Created'}, 200
                else:
                    return {'status': 'wrong answer', 'nextalias': None}, 200
            elif user.levelId > level.levelNo:
                ans = request.data['ans']
                if ans == level.ans:
                    # user = Player.query.filter(Player.email == info['email']).first()
                    user = session.query(Player).filter(Player.email == info['email']).first()
                    nextlevelno = level.levelNo + 1
                    # level = Level.query.filter(Level.levelNo == nextlevelno).first()
                    level = session.query(Level).filter(Level.levelNo == nextlevelno).first()
                    session.close()
                    if level:
                        return {'status': 'success', 'nextalias': level.name}, 200
                    else:
                        return {'status': 'failure', 'msg': 'Level Not Created'}, 200
                else:
                    return {'status': 'wrong answer', 'nextalias': None}, 400
            else:
                return {'status': 'not accessible', 'nextalias': None}, 401
        else:
            return {'status': 'invalid access'}, 401

            

@obscura.route('/getToken/', methods = ['POST','GET'])
def generatetoken():
    '''
    generate token after verifying the details of the user
    '''
    if request.method == 'POST':
        token = request.data['token']
        provider = request.data['provider']
        info = validate_token(token, provider)
        # user = Player.query.filter(Player.email == info['email']).first()
        user = session.query(Player).filter(Player.email == info['email']).first()
        if user:
            if info['email'] == user.email:
                jwt = tokenGenerate(info['email'])
                return {'backend':info['email'], 'token':jwt, 'status':'success', 'provider':provider}, 200
        else:
            return {'backend':info['email'], 'status':'failure', 'name':info['name'], 'picture':info['picture'], 'provider': provider }, 200
    return {'error':'token not recieved'}, 400

@obscura.route('/crreateLevel/', methods = ['POST', 'GET', 'PATCH'])
def createLevel():
    '''
    Creates the Level
    '''
    if request.method == 'POST':
        info = Level(request.data['name'], request.data['levelNo'], request.data['nextUrl'], request.data['picture'], request.data['html'], request.data['js'], request.data['hint'], request.data['ans'])
        session.add(info)
        session.commit()
        session.close()
        return {'status':'created'}, 201
    return {'status':'enter level details'}, 200

@obscura.route('/levelList/', methods = ['GET'])
def levelList():
    '''
    Provides the Cleared Level List
    '''
    if request.headers['auth']:             
        info = decoder()
        # user = Player.query.filter(Player.email == info['email']).first()
        # level = Level.query.filter(Level.levelNo <= user.levelId)
        user = session.query(Player).filter(Player.email == info['email']).first()
        level = session.query(Level).filter(Level.levelNo <= user.levelId)
        session.close()
        array = []
        if (1507289400 - time.time() < 0):
            for clearedLevel in level:
                data = {'name': clearedLevel.name, 'levelNo': clearedLevel.levelNo}
                array.append(data)
            return array, 200
        else:
            return array, 200
    else:
        return {'status': 'invalid access'}, 200      
