from flask import Response
from flask_restful import Resource, reqparse
from DatabaseConnector import select_from_db, insert_to_db


# Class for processing requests for register
class Register(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password_hash', type=str)
        parser.add_argument('role', type=str)
        data = parser.parse_args()

        # request to database - check user with same email
        query = f'''SELECT * FROM user WHERE email = "{data['email']}"'''
        info = select_from_db(query)

        if len(info) != 0:
            # email already used
            return Response('email already used', status=409)

        # request to database - register new user
        query = f'''INSERT INTO user(username, email, password_hash, role)
                VALUES (
                "{data['username']}",
                "{data['email']}",
                "{data['password_hash']}",
                "{data['role']}"
                );'''
        insert_to_db(query)

        return Response('ok', status=200)
