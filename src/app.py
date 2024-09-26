"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Vehicle, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize())

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = get_current_user()
    favorites = {
        "favorite_planets": [planet.serialize() for planet in user.favorite_planets],
        "favorite_characters": [character.serialize() for character in user.favorite_characters],
        "favorite_vehicles": [vehicle.serialize() for vehicle in user.favorite_vehicles]
    }
    
    return jsonify(favorites), 200
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password', 'name')):
        abort(400, description="Missing fields")
    
    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(username=data['username']).first():
        abort(400, description="Email or Username already exists")
    
    user = User(
        username=data['username'],
        email=data['email'],
        name=data['name']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])
    if 'name' in data:
        user.name = data['name']
    
    db.session.commit()
    return jsonify(user.serialize())
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
# Planet Endpoints
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize())
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not all(k in data for k in ('name', 'climate', 'terrain', 'population')):
        abort(400, description="Missing fields")
    
    planet = Planet(
        name=data['name'],
        climate=data['climate'],
        terrain=data['terrain'],
        population=data['population']
    )
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 201
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return '', 204
# Character Endpoints
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters])
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get_or_404(character_id)
    return jsonify(character.serialize())
@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    if not all(k in data for k in ('name', 'species', 'homeworld')):
        abort(400, description="Missing fields")
    
    character = Character(
        name=data['name'],
        species=data['species'],
        homeworld=data['homeworld']
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 201
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    return '', 204
# Vehicle Endpoints
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles])
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.serialize())
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not all(k in data for k in ('name', 'model', 'hp')):
        abort(400, description="Missing fields")
    
    vehicle = Vehicle(
        name=data['name'],
        model=data['model'],
        hp=data['hp']
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.serialize()), 201
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204
# Favorite Endpoints
@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    planet_id = data.get('planet_id')
    planet = Planet.query.get_or_404(planet_id)
    
    if planet not in user.favorite_planets:
        user.favorite_planets.append(planet)
        db.session.commit()
    
    return jsonify(user.serialize())
@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    character_id = data.get('character_id')
    character = Character.query.get_or_404(character_id)
    
    if character not in user.favorite_characters:
        user.favorite_characters.append(character)
        db.session.commit()
    
    return jsonify(user.serialize())
@app.route('/favorites/vehicles/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    if vehicle not in user.favorite_vehicles:
        user.favorite_vehicles.append(vehicle)
        db.session.commit()
    
    return jsonify(user.serialize())
@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)
    
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
    
    return jsonify(user.serialize())
@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = User.query.get_or_404(user_id)
    character = Character.query.get_or_404(character_id)
    
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
    
    return jsonify(user.serialize())

@app.route('/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
def remove_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get_or_404(user_id)
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    if vehicle in user.favorite_vehicles:
        user.favorite_vehicles.remove(vehicle)
        db.session.commit()
    
    return jsonify(user.serialize())
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
