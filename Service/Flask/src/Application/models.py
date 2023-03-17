import copy
import crypt
import datetime
import logging
import random
import string
from collections import UserDict

from bson import ObjectId
from config import Global
from Extensions import flask_pymongo
from marshmallow import ValidationError

__author__ = 'lonnstyle'

logger = logging.getLogger(Global.LOGGER_NAME)


class User(UserDict):
    """
    Represent user, implementing proper methods
    """

    _data = {
        '_id': None,
        'avatar': None,
    }

    def __init__(self,_id=None, data=None, email=None, name=None):
        super().__init__(copy.deepcopy(self._data))
        if data is not None:
            self.update(data)
    
        find_by = {}
        # if _id is not None:
        #     # _id = _id if isinstance(_id, ObjectId) else ObjectId(_id)
        #     find_by['_id'] = _id
        if email is not None:
            find_by['email'] = email.lower()
        if name is not None:
            find_by['name'] = name
        if len(find_by) > 0:
            user = flask_pymongo.db.users.find_one(find_by)
            if user is not None:
                self.update(user)

    @classmethod
    def create_from(cls,data):
        if 'password' in data:
            data['password_hash'] = cls.generate_password(data['password'])
            del data['password']
        # data['created_at'] = datetime.datetime.utcnow()
        user = cls(data=data)
        return user

    @property
    def id(self):
        return self.data.get('_id', None)

    @staticmethod
    def generate_password(password):
        return str.encode(crypt.crypt(password, salt=crypt.METHOD_SHA512))
    
    def check_password(self,inp):
        password_hash = self.data.get('password_hash', None)
        if password_hash is None:
            return False
        password_hash = password_hash.decode()
        return crypt.crypt(inp, password_hash) == password_hash
    
    def insert(self):
        del self.data['_id']
        self.data['_id'] = flask_pymongo.db.users.insert_one(self.data).inserted_id

    def __str__(self):
        return "<%s (id:%s, name:%s)>" % (self.__class__.__name__,
                                                    self.id,
                                                    self.get('name', None))

    def dump_short(self):
        fields = ['_id', 'name']
        data = copy.deepcopy(self.data)
        for key in list(data.keys()):
            if key not in fields:
                del data[key]
        return data