import json
import logging
from json import JSONEncoder
from pprint import pprint

from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from flask import request
from marshmallow import ValidationError

from .schemas import Registration

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class RegistrationView(Classy42):
    decorators = []
    trailing_slash = False

    def post(self):
        j_req = request.get_json()
        user = Registration(strict=True).load(j_req).data
        return {'payload': {'user': user.dump_short()}}