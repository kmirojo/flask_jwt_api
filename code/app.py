from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

# __name__ → Gives each file a unique name
app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

# /auth -> Manages the users authorization
jwt = JWT(app, authenticate, identity)

# In-memory DB
items = []


# class MyClass(AnotherClass) → MyClass inherits from AnotherClass
class Item(Resource):

    # Format the request data to only work (in this case) with "price" field
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    # this decorator makes the JWT authorization to be required for executing the following method
    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # filter(filtering function, list of items filtering)
        # filter() will return a filter object
        # next() will return the next item from the iterator, in this case, the item
        item = next(filter(lambda x: x['name'] == name, items), None)

        return {'item': item}, 200 if item else 404

    def post(self, name):
        # lambda is a small anonymous function which can only have one expression
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)  # Add item to DB
        return item, 201

    def delete(self, name):
        # Override global items list removing (not filtering) the selected item
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "Item '{}' was deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            # If the item doesn't exists, it's created
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


# API
# http://localhost:5000/student/Juan
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
