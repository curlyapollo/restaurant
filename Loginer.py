import datetime
import jwt
from flask import Response
from flask_restful import Resource, reqparse


from DatabaseConnector import select_from_db, insert_to_db


# Class for processing requests for login
class Loginer(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password_hash', type=str)
        data = parser.parse_args()

        # request to database - find user's info
        query = f'''SELECT * FROM user WHERE email = "{data['email']}"'''
        info = select_from_db(query)
        print(info)

        if len(info) != 1 or len(info[0]) < 4 or info[0][3] != data['password_hash']:
            # email or password is incorrect
            return Response('bad users info', status=409)

        # generate jwt to session info
        session_token = jwt.encode(payload=data, key='restaurant_key')
        expires_at = str(datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=1))

        # request to database - add session
        query = f'''INSERT INTO session(user_id, session_token, expires_at)
                    VALUES (
                    {info[0][0]},
                    "{session_token}",
                    "{expires_at}"
                    );'''
        insert_to_db(query)

        # request to database - get session id
        query = f'''SELECT * FROM session WHERE session_token = "{session_token}"'''
        res = select_from_db(query)

        return Response(str(res[0][0]), status=200)
