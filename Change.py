import json

from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db, insert_to_db


# Class for change count of dish
class Change(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('delta', type=int)
        parser.add_argument('id', type=int)
        data = parser.parse_args()

        # request to database - change dish
        if data['delta'] == 0:
            query = f'UPDATE dish SET quantity = 0 WHERE id = {data["id"]}'
        else:
            query = f'UPDATE dish SET quantity = quantity + {data["delta"]} WHERE id = {data["id"]}'
        insert_to_db(query)

        # request to database - get dish id
        query = f'''SELECT * FROM dish WHERE id = {data["id"]}'''
        res = select_from_db(query)

        result = {'name': res[0][1], 'count': res[0][4]}
        return Response(response=json.dumps(result), status=200)