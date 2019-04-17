from flask import Flask, request
from flask_restful import Resource, Api

# pip install Flask-JWT - JSON Web Token
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# app is a Flask app in the current namespace
app = Flask(__name__)
# Assign secret key
app.secret_key = 'stub'
# Create and instance of api from the app
api = Api(app)

# create jwt using app, authenticate and identity methods
jwt = JWT(app, authenticate, identity) # /auth

# List to contain the JSON dictionary of the data
items = []

class Item(Resource):
    ''' Item method - get and post '''
    @jwt_required() #Decorator to require authentication
    def get(self, name):
        # For all items, if item == name, return first item.  If none, return none
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    # Post method  - add new item with fixed price
    def post(self, name):
        # Names must be unique.  If item already exists, raise an error.
        if next(filter(lambda x: x['name'] == name, items), None):
            return{'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json() # force=True In case header is not set, or silent=True - do nothing
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # Created

    def delete(self, name):
        # User global items variable in lambda to define local items
        global items
        # Recreate items list with all items except the one to delete
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

class ItemList(Resource):
    ''' ItemList method - gets all items '''
    def get(self):
        return {'items': items}


# Add the resouce to the api
api.add_resource(Item, '/item/<string:name>') # Endpoint for item
api.add_resource(ItemList, '/items') # Endpoint for Item list

# Run the app
app.run(port=5000, debug=True) # Log all the good stuff.
