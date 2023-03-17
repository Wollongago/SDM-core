import logging
from copy import deepcopy

from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Marshmallow import Fields
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validates, validates_schema
from marshmallow.utils import isoformat

logger = logging.getLogger('StudyBuddy')

class Review:
    fields = [
        '_id',
        'tutor',
        'user',
        'rating',
        'comment',
    ]

    def dump(self,data):
        # skip the fields if they are None
        return {k: v for k, v in data.items() if k in self.fields and v is not None}
    
    def dump_many(self,data_list):
        return [self.dump(data) for data in data_list]
    
class ReviewSchema(Schema):
    _id = Fields.String(dump_only=True)
    # user who is reviewing
    user = Fields.String(required=True)
    rating = fields.Integer(required=True)
    comment = fields.String(required=False)
    # user who is being reviewed
    target = fields.String(required=True)
    
    
    @validates('user')
    def validate_user(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value)}):
            raise ValidationError('User does not exist', 'user')
    
    @validates_schema
    def validate_schema(self, data):
        if data['user'] == data['target']:
            raise ValidationError('User cannot review themselves', 'user')
    
    
    @post_load
    def post_load(self, data):
        return Review().dump(data)