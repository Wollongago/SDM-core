import logging

from Application.models import User
from Extensions import flask_pymongo
from flask import g
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validates, validates_schema

logger = logging.getLogger('Api')

class Registration(Schema):
    email = fields.Email(required=True,error_messages={'required': 'Email is required'})
    password = fields.String(required=True,error_messages={'required': 'Password is required'})
    password_second = fields.String(required=True,error_messages={'required': 'Password confirmation is required'})
    name = fields.String(required=True,error_messages={'required': 'Name is required'})

    @validates('password')
    def validate_password(self, value):
        if len(value) < 5:
            raise ValidationError('Password is too short', 'password')
        
    @validates_schema
    def validate_passwords(self, data):
        if data['password'] != data['password_second']:
            raise ValidationError('Passwords do not match', ['password', 'password_second'])
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('Name is too short', 'name')
        if len(value) > 50:
            raise ValidationError('Name is too long', 'name')
        if not value.isalnum():
            raise ValidationError('Name must contain only letters and numbers', 'name')
        
    @pre_load
    def lower_email(self, data):
        data['email'] = data['email'].lower()
        return data
    
    @post_load
    def create_user(self, data):
        del data['password_second']
        exists = flask_pymongo.db.user.find_one({'email': data['email']})
        if exists is not None:
            raise ValidationError('User with this email already exists', 'email')
        
        user = User.create_from(data)
        user.insert()
        return user