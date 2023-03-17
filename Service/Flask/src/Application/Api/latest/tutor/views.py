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

class TutorView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}
    
    # POST review tutor
    @route('/<tutor_id>/review', methods=['POST'])
    def review_tutor(self,tutor_id):
        j_req = request.get_json()
        tutor = flask_pymongo.db.tutors.find_one({"_id": ObjectId(tutor_id)})
        if tutor is None:
            return {'error': 'Tutor not found'}
        j_req['tutor'] = tutor_id
        cnt = flask_pymongo.db.reviews.insert_one(j_req).inserted_id
        if cnt is None:
            return {'error': 'Review not created'}
        return {'payload': {'review': {'_id': str(cnt)}}}