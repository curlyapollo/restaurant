import json

from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db


# Class for printing menu
class Menu(Resource):
    def post(self) -> Response:

        # request to database - find user's session
        query = f'''SELECT * FROM dish'''
        info = select_from_db(query)

        res = {}
        for item in info:
            if item[4] > 0:
                res[item[1]] = {'price': item[3], 'description': item[2], 'id': item[0]}
        print(res)
        return Response(status=200, response=json.dumps(res, ensure_ascii=False, default=str))
