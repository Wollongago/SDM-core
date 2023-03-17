import logging

from Extensions.Nestable.Classy import Classy42

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class UserView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}