# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {
        'title': 'Welcome to the pet directory!',
        'body': 'This is the body of the response.'
    }
    return make_response(body, 200)


@app.route('/demo_json')
def demo_json():
    pet_dict = {'id': 1,
            'name': 'Fido',
            'species': 'Dog'
            }
    return make_response(pet_dict, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter_by(id=id).first()
    if pet:
        body = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        status = 200
    else:
        body = {
            'message': f'Pet {id} not found'
        }
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pets_by_species(species):
    pets = []
    for pet in Pet.query.filter_by(species=species):
        pets.append({
            'id': pet.id,
            'name': pet.name,
           'species': pet.species
        })
    if pets:
        body = {
            'count': len(pets),
            'pets': pets
        }
        status = 200

    return make_response(body, status) 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
