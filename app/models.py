from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    restaurant_pizzas = db.relationship('Restaurant_Pizza', backref='restaurant')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'restaurant_pizzas': [{'id': pizza.id, 'price': pizza.price, 'pizza': {'id': pizza.pizza.id, 'name': pizza.pizza.name, 'ingredients': pizza.pizza.ingredients}} for pizza in self.restaurant_pizzas]
        }

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant_pizzas = db.relationship('Restaurant_Pizza', backref='pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'restaurant_pizzas': [{'id': pizza.id, 'price': pizza.price, 'restaurant': {'id': pizza.restaurant.id, 'name': pizza.restaurant.name, 'address': pizza.restaurant.address}} for pizza in self.restaurant_pizzas]
        }

class Restaurant_Pizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza': {'id': self.pizza.id, 'name': self.pizza.name, 'ingredients': self.pizza.ingredients},
            'restaurant': {'id': self.restaurant.id, 'name': self.restaurant.name, 'address': self.restaurant.address}
        }


