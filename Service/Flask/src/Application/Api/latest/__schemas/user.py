import logging
from copy import deepcopy

from Extensions import flask_pymongo
from Extensions.Marshmallow import Fields
from flask import get_flashed_messages
from marshmallow import Schema, fields
from marshmallow.utils import isoformat

logger = logging.getLogger('StudyBuddy')

class UserDump:
    fields = [
        '_id',
        'name',
        'email',
        'avatar',
    ]

    def dump(self,data):
        # skip the fields if they are None
        return {k: v for k, v in data.items() if k in self.fields and v is not None}
    
    def dump_many(self,data_list):
        return [self.dump(data) for data in data_list]