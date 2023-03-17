from Extensions.Nestable import NestableBlueprint

__author__ = 'lonnstyle'

collection = NestableBlueprint('User',__name__,url_prefix='/session')
collection.register_collection(__file__)