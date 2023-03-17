import logging
import time

from Application.models import Session
from bson import ObjectId
from Extensions import flask_pymongo
from flask import g
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validates, validates_schema

logger = logging.getLogger('Api')

class TutorSession(Schema):
    tutor = fields.String(required=True,error_messages={'required': 'Tutor is required'})
    subject = fields.String(required=True,error_messages={'required': 'Subject is required'})
    # start and end time should in timestamp
    start = fields.Integer(required=True,error_messages={'required': 'Start time is required'})
    end = fields.Integer(required=True,error_messages={'required': 'End time is required'})
    price = fields.Float(required=True,error_messages={'required': 'Price is required'})
    description = fields.String(required=True,error_messages={'required': 'Description is required'})
    max_students = fields.Integer(required=True,error_messages={'required': 'Max students is required'})

    @validates('tutor')
    def validate_tutor(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value), 'tutor': True}):
            raise ValidationError('Tutor does not exist', 'tutor')
        
    @validates('start')
    def validate_start(self, value):
        # the start time should be in the future
        if value < int(time.time()):
            raise ValidationError('Start time should be in the future', 'start')
        
    @validates_schema
    def validate_time(self, data):
        # the end time should be after the start time for at least 30 minutes
        if data['end'] - data['start'] < 1800:
            raise ValidationError('Session should be at least 30 minutes long', ['start', 'end'])
        
    @validates('price')
    def validate_price(self, value):
        if value < 0:
            raise ValidationError('Price cannot be negative', 'price')
    
    @validates('max_students')
    def validate_max_students(self, value):
        if value < 1:
            raise ValidationError('Max students cannot be less than 1', 'max_students')
        
    @validates('description')
    def validate_description(self, value):
        if len(value) < 10:
            raise ValidationError('Description is too short', 'description')
        if len(value) > 500:
            raise ValidationError('Description is too long', 'description')
        
    @post_load
    def create_session(self, data):
        session = Session.create_from(data)
        session.insert()
        return session
    
class SessionSearch(Schema):
    # search on given arguments, if not given, search on all sessions
    tutor = fields.String(required=False)
    subject = fields.String(required=False)
    start = fields.Integer(required=False)
    end = fields.Integer(required=False)
    price = fields.Float(required=False)
    max_students = fields.Integer(required=False)

    @post_load(pass_original=True)
    def search_session(self, data, original_data):
        # create aggregation pipeline
        pipeline = []
        # match on tutor
        if 'tutor' in original_data:
            pipeline.append({'$match': {'tutor': ObjectId(data['tutor'])}})
        # match on subject
        if 'subject' in original_data:
            pipeline.append({'$match': {'subject': data['subject']}})
        # match on price
        if 'price' in original_data:
            pipeline.append({'$match': {'price': {'$lte': data['price']}}})
        # match on max students
        if 'max_students' in original_data:
            pipeline.append({'$match': {'max_students': {'$gte': data['max_students']}}})
        # match on start time
        if 'start' in original_data:
            pipeline.append({'$match': {'start': {'$gte': data['start']}}})
        # match on end time
        if 'end' in original_data:
            pipeline.append({'$match': {'end': {'$lte': data['end']}}})
        
        # we don't have any banning system yet, so we don't need to filter out banned users
        # lookup user info and check if the user is banned
        # pipeline.extend([
        #     {'$lookup': {
        #         'from': 'users',
        #         'localField': 'tutor',
        #         'foreignField': '_id',
        #         'as': 'tutor'}},
        #     {'$match': {'tutor.banned': {'$ne': True}}}
        # ])
