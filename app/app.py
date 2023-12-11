#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizza



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "This Server is up"

@app.route('/restaurants')
def restaurant():

    restaurants = []

    for rest in Restaurant.query.all():
        restaurant = {
            "id":rest.id,
            "name": rest.name,
            "address":rest.address,
            "restaurant_pizzas":rest.restaurant_pizzas
        }
        restaurants.append(restaurant)

    response = make_response(
        jsonify(restaurants),
        200
    )
    return response

@app.route('/restaurants/<int:id>', methods=['GET','DELETE'])
def single_restaurant(id):

    if request.method == 'GET':
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                    }),
                404
            )
            return response
        elif restaurant:

            response = make_response(
                jsonify(restaurant),
                200
            )
            return response
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.filter_by(id=id).first()
        restaurant.query.delete()
        db.session.commit()

        response = make_response(
            jsonify({
                "Delete_successful" : True,
                "message" : "Restaurant successfully deleted."
            }),
            200
        )
        return response

@app.route('/pizzas')
def pizzas():

    pizza = [pizza.to_dict() for pizza in Pizzas.query.all()]

    response = make_response(
        jsonify(pizza),
        200
    )
    return response

@app.route('/restaurant_pizzas', methods=['GET','POST'])
def restaurant_pizzas():

    data = request.get_json()

    new_post = {
        "pizza_id": data["pizza_id"],
        "restaurant_id": data["restaurant_id"],
        "price": data["price"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"]
    }

    db.session.add(new_post)
    db.session.commit()

    response = make_response(
        jsonify(new_post.to_dict()),
        201
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)




