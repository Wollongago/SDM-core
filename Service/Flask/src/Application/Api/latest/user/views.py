import logging

from Application.Api.latest.__schemas.user import UserDump
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
