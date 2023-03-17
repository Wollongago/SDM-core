import logging

from Application.Api.latest.__schemas.user import UserDump
from Application.models import User
from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class UserView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}
    
    @route('/<user_id>', methods=['PUT'])
    def update_user(self,user_id):
        user = flask_pymongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            return {'error': 'User not found'}
        j_req = request.get_json()
        cnt = flask_pymongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": j_req}).modified_count
        if cnt == 0:
            return {'error': 'User not updated'}
        user = flask_pymongo.db.users.find_one({"_id": ObjectId(user_id)})
        schema = UserDump()
        user = schema.dump(user)
        return {'payload': {'user': user}}

    # delete user
    @route('/<user_id>', methods=['DELETE'])
    def delete_user(self,user_id):
        cnt = flask_pymongo.db.users.delete_one({"_id": ObjectId(user_id)}).deleted_count
        if cnt == 0:
            return {'error': 'User not deleted'}
        return {'payload': {'user': {'_id': user_id}}}
    
    # user login
    @route('/login', methods=['POST'])
    def login(self):
        j_req = request.get_json()
        user = User(email=j_req['email'])
        if user is None:
            return {'error': 'User not found'}
        if not user.check_password(j_req['password']):
            return {'error': 'Wrong password'}
        user = user.dump_short()
        return {'payload': {'user': user}}
    
    # user logout
    @route('/logout', methods=['POST'])
    def logout(self):
        return {'payload': {'user': None}}
    
    # review user
    @route('/<user_id>/review', methods=['POST'])
    def review_user(self,user_id):
        j_req = request.get_json()
        j_req['reviewer_id'] = user_id
        id = flask_pymongo.db.reviews.insert_one(j_req).inserted_id
        if id is None:
            return {'error': 'Review not created'}
        return {'payload': {'review': {'_id': id}}}