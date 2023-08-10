#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


class Heroes(Resource):
    def get(self):
        heroes = [hero.to_dict(
            rules=('-hero_powers',)) for hero in Hero.query.all()]
        return make_response(heroes, 200)

    def post(self):
        fields = request.get_json()
        try:
            hero_power = HeroPower(
                strength=fields.get('strength'),
                power_id=fields.get('power_id'),
                hero_id=fields.get('hero_id'),
            )
            db.session.add(hero_power)
            db.session.commit()
            return make_response(hero_power.to_dict(), 200)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)


api.add_resource(Heroes, "/heroes")


class HeroesById(Resource):

    def get(self, id):
        hero = Hero.query.filter_by(id=id).one_or_none()

        if hero is None:
            return make_response({'error': 'Hero not found'}, 404)

        return make_response(hero.to_dict(), 200)


api.add_resource(HeroesById, "/heroes/<int:id>")


class Powers(Resource):
    def get(self):
        powers = [power.to_dict(
            rules=('-hero_powers',)) for power in Power.query.all()]
        return make_response(powers, 200)


api.add_resource(Powers, "/powers")


class PowersById(Resource):

    def get(self, id):
        power = Power.query.filter(Power.id == id).one_or_none()

        if power is None:
            return make_response({'error': 'Power not found'}, 404)

        return make_response(power.to_dict(rules=('-hero_powers',)), 200)

    def patch(self, id):
        power = Power.query.filter(Power.id == id).one_or_none()

        if power is None:
            return make_response({'error': 'Power not found'}, 404)

        fields = request.get_json()
        try:
            setattr(power, 'description', fields['description'])

            db.session.add(power)
            db.session.commit()
            return make_response(power.to_dict(rules=('-hero_powers',)), 200)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)


api.add_resource(PowersById, "/powers/<int:id>")


class HeroPowers(Resource):
    def post(self):
        fields = request.get_json()
        try:
            hero_power = HeroPower(
                strength=fields.get('strength'),
                power_id=fields.get('power_id'),
                hero_id=fields.get('hero_id'),
            )
            db.session.add(hero_power)
            db.session.commit()
            return make_response(hero_power.to_dict(), 200)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)


api.add_resource(HeroPowers, "/hero_powers")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
