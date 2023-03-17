from bson import ObjectId
from Extensions import flask_pymongo
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validates, validates_schema


class Booking(Schema):
    session = fields.String(required=True,error_messages={'required': 'Session is required'})
    user = fields.String(required=True,error_messages={'required': 'User is required'})
    paid = fields.Boolean(required=False,missing=False)

    @validates('session')
    def validate_session(self, value):
        if not flask_pymongo.db.sessions.find_one({'_id': ObjectId(value)}):
            raise ValidationError('Session does not exist', 'session')
    
    @validates('user')
    def validate_user(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value)}):
            raise ValidationError('User does not exist', 'user')