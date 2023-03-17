import logging

from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request

from .schemas import Booking

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class BookingView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}
    
    # make booking
    def post(self):
        j_req = request.get_json()
        booking = Booking(strict=True).load(j_req).data
        return {'payload': {'booking': booking.dump_short()}}
    
    # delete booking
    @route('/<booking_id>', methods=['DELETE'])
    def delete_booking(self,booking_id):
        cnt = flask_pymongo.db.bookings.delete_one({"_id": ObjectId(booking_id)}).deleted_count
        if cnt == 0:
            return {'error': 'Booking not deleted'}
        return {'payload': {'booking': {'_id': booking_id}}}