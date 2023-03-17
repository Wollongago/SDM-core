from Extensions.Nestable import NestableBlueprint

__author__ = 'lonnstyle'

collection = NestableBlueprint('v1', __name__, url_prefix='/booking')
collection.register_collection(__file__)
