import logging

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
            return {'error': 'User not found'}, 404
        cnt = flask_pymongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": request.get_json()}).modified_count
        if cnt == 0:
            return {'error': 'User not updated'}, 500
        return {'payload': {'user': user}}
