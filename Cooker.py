from flask import Response
from flask_restful import Resource

from DatabaseConnector import select_from_db, insert_to_db


# Class for cook the dish
class Cooker(Resource):
    def post(self) -> Response:

        # request to database - find uncooked dish
        query = f'''SELECT * FROM orders WHERE status = "принят"'''
        res = select_from_db(query)
        if len(res) == 0:
            return Response(status=409)

        # request to database - cook dish
        query = f'UPDATE orders SET status = "готов" WHERE id = {res[0][0]}'
        insert_to_db(query)

        # request to database - get user name
        query = f'''SELECT * FROM user WHERE id = {res[0][1]}'''

        res = select_from_db(query)[0]
        return Response(status=200, response=f'{res[1]}')