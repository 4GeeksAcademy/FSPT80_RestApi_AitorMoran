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
from models import db, People, Favorites, Planets, Planetforites
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

#obtener people________________________

@app.route('/people', methods=['GET'])
def get_people():
    data = People.query.all() 
    people_list = [el.serialize() for el in data] 

    return jsonify(people_list), 200

#obtener people id________________________

@app.route('/people/<int:id>', methods=['GET'])
def get_one(id):
    data = People.query.get(id) 
    if not data: return jsonify({"error": "Persona no encontrada"}), 404
    
    return jsonify(data.serialize()), 200

#añadir people________________________

@app.route('/newpeople', methods=['POST'])
def new_people():
    try:
        data = request.json
        
        newPeople = People(
            id = data['id'],
            name = data['name'],
            lastname = data['lastname'],
            side = data['side']
        )
        db.session.add(newPeople)
        db.session.commit()
        return jsonify("Personaje Creado"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

#eliminar people________________________

@app.route('/deletepeople/<int:id>', methods=['DELETE'])
def delete_people(id):
    try:
        data = People.query.get(id)
        if data is None:
            raise Exception("No se encontró el sujeto")
        
        db.session.delete(data)
        db.session.commit()
        return jsonify({"message": "Sujeto eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


#añadir people a favoritos________________________

@app.route('/favorites/<int:person_id>', methods=['POST'])
def add_favorite(person_id):
    try:
        data = request.json
        
        person = People.query.get(person_id)
        if not person:
            raise Exception("Persona no encontrada")
        
        new_favorite = Favorites(
            person_id = person_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify("Sujeto añadido a favoritos"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

#obtener planets________________________

@app.route('/planets', methods=['GET'])
def get_planet():
    data = Planets.query.all() 
    planet_list = [el.serialize() for el in data] 

    return jsonify(planet_list), 200

#obtener planets id________________________

@app.route('/planets/<int:id>', methods=['GET'])
def get_ones(id):
    data = Planets.query.get(id) 
    if not data: return jsonify({"error": "Planeta no encontrada"}), 404
    
    return jsonify(data.serialize()), 200

#añadir planets________________________

@app.route('/newplanet', methods=['POST'])
def new_planet():
    try:
        data = request.json
        
        new_planet = Planets(
            id = data['id'],
            name = data['name'],
            terrain = data['terrain'],
            population = data['population'],
            galaxy = data['galaxy']
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify("Planeta Creado"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

#eliminar planets________________________

@app.route('/deleteplanet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    try:
        data = Planets.query.get(id)
        if data is None:
            raise Exception("No se encontró el planeta")
        
        db.session.delete(data)
        db.session.commit()
        return jsonify({"message": "Planeta eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


#añadir planets a favoritos________________________

@app.route('/planetforites/<int:planet_id>', methods=['POST'])
def add_planetforites(planet_id):
    try:
        data = request.json
        
        planet = Planets.query.get(planet_id)
        if not planet:
            raise Exception("Planeta no encontrado")
        
        new_favorite = Planetforites(
            planet_id = planet_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify("Planeta añadido a favoritos"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400












@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
