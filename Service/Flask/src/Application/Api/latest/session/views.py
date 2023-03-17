import logging

from Application.Api.latest.session.schemas import SessionSearch
from Application.models import Session
from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class SessionView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}
    
    # TODO: decorator for checking user is tutor
    # not implementing cuz we don't have login session yet
    def post(self):
        # create tutor session
        j_req = request.get_json()
        session = Session(strict=True).load(j_req).data
        return {'payload': {'session': session.dump_short()}}
    
    @route('/<session_id>', methods=['PUT'])
    def update_session(self,session_id):
        session = flask_pymongo.db.sessions.find_one({"_id": ObjectId(session_id)})
        if session is None:
            return {'error': 'Session not found'}
        j_req = request.get_json()
        cnt = flask_pymongo.db.sessions.update_one({"_id": ObjectId(session_id)}, {"$set": j_req}).modified_count
        if cnt == 0:
            return {'error': 'Session not updated'}
        session = flask_pymongo.db.sessions.find_one({"_id": ObjectId(session_id)})
        session = Session(strict=True).load(session).data
        return {'payload': {'session': session.dump_short()}}
    
    @route('/<session_id>', methods=['DELETE'])
    def delete_session(self,session_id):
        cnt = flask_pymongo.db.sessions.delete_one({"_id": ObjectId(session_id)}).deleted_count
        if cnt == 0:
            return {'error': 'Session not deleted'}
        return {'payload': {'session': {'_id': session_id}}}    
    
    # search sessions
    @route('/search', methods=['GET'])
    def search_sessions(self):
        args = request.args.to_dict()
        pipeline = SessionSearch(strict=True).load(args).data
        sessions = flask_pymongo.db.sessions.aggregate(pipeline)
        return {'payload': {'sessions': list(sessions)}}
    
    # get session
    @route('/<session_id>', methods=['GET'])
    def get_session(self,session_id):
        session = flask_pymongo.db.sessions.find_one({"_id": ObjectId(session_id)})
        if session is None:
            return {'error': 'Session not found'}
        session = Session(strict=True).load(session).data
        return {'payload': {'session': session.dump_short()}}