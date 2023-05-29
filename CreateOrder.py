from flask import Response
from flask_restful import Resource, reqparse

from DatabaseConnector import select_from_db, insert_to_db


# Class for creating new order
class CreateOrder(Resource):
    def post(self) -> Response:
        # get request info
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        parser.add_argument('id', type=int)
        x = parser.parse_args()
        x['data'] = map(int, x['data'].split('_'))

        # request to database - add order
        query = f'''INSERT INTO orders(user_id, status)
                        VALUES (
                        {x['id']},
                        "принят"
                        );'''
        insert_to_db(query)
        query = f'''SELECT * FROM orders WHERE user_id = {x['id']}'''
        res = select_from_db(query)
        order_id = res[-1][0]

        for item in x['data']:
            # get dish info
            query = f'''SELECT * FROM dish WHERE id = {item}'''
            res = select_from_db(query)
            # add one dish to order_dish
            query = f'''INSERT INTO order_dish(order_id, dish_id, quantity, price)
                                    VALUES (
                                    {order_id},
                                    {res[-1][0]}, 1, 
                                    {res[-1][3]}
                                    );'''
            insert_to_db(query)

            # update dish info
            query = f'UPDATE dish SET quantity = quantity - 1 WHERE id = {item}'
            insert_to_db(query)
        return Response(response=f'{order_id}', status=200)