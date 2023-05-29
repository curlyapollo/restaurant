import json

from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db, insert_to_db


# Class for adding new dish
class Adder(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=int)
        parser.add_argument('disc', type=int)
        parser.add_argument('cost', type=int)
        parser.add_argument('cou', type=int)
        data = parser.parse_args()

        # request to database - insert dish
        query = f'''INSERT INTO dish(name, description, price, quantity, is_available)
                    VALUES ("{data['name']}", "{data['disc']}", {data['cost']}, {data['cou']}, true)'''
        insert_to_db(query)

        # request to database - get dish id
        query = f'''SELECT * FROM dish WHERE id = {data["id"]}'''
        res = select_from_db(query)

        result = {'name': res[0][1], 'count': res[0][4]}
        return Response(response=json.dumps(result), status=200)


