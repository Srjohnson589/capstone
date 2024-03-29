from . import auth_api
from flask import request, jsonify
from app.models import db, User
from werkzeug.security import check_password_hash

# Create User
@auth_api.post('/signup')
def signup_api():
    '''
    payload should include
    {
    "username": "string",
    "password": "string"
    }
    '''
    data = request.get_json()
    queried_user = User.query.filter(User.username == data['username']).first()
    if not queried_user and len(data['username'].strip()) > 0:
        new_user = User(username = data['username'], password = data['password'])
        new_user.save()
        return jsonify({
            'status': 'ok',
            'message': 'User was successfully created'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Username already exists'
        })

@auth_api.post('/login')
def login_api():
    '''
    payload should include
    {
    "username": "string",
    "password": "string"
    }
    '''
    data = request.get_json()
    queried_user = User.query.filter(User.username == data['username']).first()
    if queried_user and check_password_hash(queried_user.password, data['password']):
        return jsonify({
            'status': 'ok',
            'message': 'Username and password are correct'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Username or password are incorrect'
        })
    
@auth_api.get('/all_users/<username>')
def get_users(username):
    queried_user = User.query.filter(User.username == username).first()
    if queried_user:
        users = User.query.filter(User.user_id != queried_user.user_id)
        notfollowing = []
        following = []
        for user in users:
            thisuser = {
                'username': user.username,
                'profile_pic': user.profile_pic
            }
            if user in queried_user.following:
                following.append(thisuser)
            else:
                notfollowing.append(thisuser)
        return jsonify({
            'status': 'ok',
            'message': 'Found users',
            'notfollowing': notfollowing,
            'following': following
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'User does not exist'
        })
    
@auth_api.post('/follow')
def follow():
    '''
    payload should include
    {
    "user": "string",
    "tofollow": "string"
    }
    '''
    data = request.get_json()
    print(data)
    queried_user = User.query.filter(User.username == data['user']).first()
    queried_to_follow = User.query.filter(User.username == data['tofollow']).first()
    if queried_user and queried_to_follow:
        queried_user.following.append(queried_to_follow)
        db.session.commit()
        return jsonify({
            'status': 'ok',
            'message': 'Following user'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'One of the users does not exist'
        })
    
@auth_api.post('/unfollow')
def unfollow():
    '''
    payload should include
    {
    "user": "string",
    "unfollow": "string"
    }
    '''
    data = request.get_json()
    print(data)
    queried_user = User.query.filter(User.username == data['user']).first()
    queried_unfollow = User.query.filter(User.username == data['unfollow']).first()
    if queried_user and queried_unfollow:
        queried_user.following.remove(queried_unfollow)
        db.session.commit()
        return jsonify({
            'status': 'ok',
            'message': 'Not following user'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'One of the users does not exist'
        })
    
@auth_api.post('/save_picture')
def save_picture():
    '''
    payload should include
    {
    "username": "string",
    "profile_pic": "string"
    }
    '''
    data = request.get_json()
    print(data)
    queried_user = User.query.filter(User.username == data['username']).first()
    if queried_user:
        queried_user.profile_pic = data['profile_pic']
        db.session.commit()
        return jsonify({
            'status': 'ok',
            'message': 'Picture updated'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'User does not exist'
        })
    
@auth_api.get('/friends_current/<username>')
def friends_current(username):
    queried_user = User.query.filter(User.username == username).first()
    if queried_user:
        friends_current = []
        for user in queried_user.following:
            for item in user.current_shelf:
                newitem = {
                    'thumbnail': item.thumbnail,
                    'username': user.username
                }
                friends_current.append(newitem)
        print(friends_current)
        return jsonify({
            'status': 'ok',
            'message': 'Found users',
            'friends_current': friends_current
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'User does not exist'
        })