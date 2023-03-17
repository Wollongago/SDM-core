from Extensions.Nestable import NestableBlueprint

__author__ = 'lonnstyle'

collection = NestableBlueprint('Tutor',__name__,url_prefix='/tutor')
collection.register_collection(__file__)