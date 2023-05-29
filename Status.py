import json

from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db


# Class to get info about order status
class Status(Resource):
    def post(self) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('ord_id', type=int)
        data = parser.parse_args()
        query = f'''SELECT * FROM orders WHERE id = {data['ord_id']}'''
        res = select_from_db(query)
        return Response(response=res[-1][2], status=200)
