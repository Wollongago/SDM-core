from bson import ObjectId
from Extensions import flask_pymongo
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validates, validates_schema


class Booking(Schema):
    session = fields.String(required=True,error_messages={'required': 'Session is required'})
    user = fields.String(required=True,error_messages={'required': 'User is required'})
    paid = fields.Boolean(required=False,missing=False)

    @validates('session')
    def validate_session(self, value):
        session = flask_pymongo.db.sessions.find_one({'_id': ObjectId(value)})
        if session is None:
            raise ValidationError('Session does not exist', 'session')
        bookings = flask_pymongo.db.booking.find({'session': ObjectId(value)}).count()
        if bookings >= session['max_students']:
            raise ValidationError('Session is full', 'session')
    
    @validates('user')
    def validate_user(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value)}):
            raise ValidationError('User does not exist', 'user')
        # check if the user has already booked this session
        if flask_pymongo.db.booking.find_one({'user': ObjectId(value),'session': ObjectId(self.context['session'])}):
            raise ValidationError('User has already booked this session', 'user')
        
    @post_load
    def post_load(self, data):
        # add the booking to the database
        cnt = flask_pymongo.db.booking.insert_one(data).inserted_id
        if cnt is None:
            raise ValidationError('Booking not created', 'booking')
        return {'payload': {'booking': {'_id': cnt}}}