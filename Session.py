import datetime
import json

from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db


# Class for processing requests for information
class Session(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', type=int)
        data = parser.parse_args()

        # request to database - find user's session
        query = f'''SELECT * FROM session WHERE id = {data['session_id']}'''
        info = select_from_db(query)
        print(info)
        print(info[-1])
        if len(info) != 1 or len(info[-1]) < 4:
            # session don't found
            return Response('bad session_id', status=404)

        if info[-1][3] <= datetime.datetime.now():
            # user's session is inactive
            return Response('session is inactive', status=409)

        # request to database - get user info
        query = f'''SELECT * FROM user WHERE id = "{info[-1][1]}"'''
        info = select_from_db(query)

        if info[0][4] == 'customer':
            role = 'гость'
        elif info[0][4] == 'chef':
            role = 'повар'
        else:
            role = 'менеджер'

        # all is ok
        res = {'role': role, 'name': info[-1][1], 'id': info[-1][0]}
        return Response(response=json.dumps(res), status=200)
