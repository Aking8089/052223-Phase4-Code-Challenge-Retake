#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
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

class Vendors(Resource):
    def get(self):
        vendors = [vendor.to_dict() for vendor in Vendor.query.all()]
        return make_response(vendors, 200)
api.add_resource(Vendors, "/vendors")

class VendorById(Resource):
    def get(self, id):
        vendor = Vendor.query.filter_by(id=id).one_or_none()
        if vendor is None:
            return make_response({'error': 'Vendor not found'}, 404)
        vendor_dict = vendor.to_dict()
        vendor_dict['vendor_sweets'] = [vs.to_dict() for vs in vendor.vendor_sweets]
        return make_response(vendor_dict, 200)
api.add_resource(VendorById, "/vendors/<int:id>")

class Sweets(Resource):
    def get(self):
        sweets = [sweet.to_dict() for sweet in Sweet.query.all()]
        return make_response(sweets, 200)
api.add_resource(Sweets, "/sweets")

class SweetById(Resource):
    def get(self, id):
        sweet = Sweet.query.filter_by(id=id).one_or_none()
        if sweet is None:
            return make_response({'error': 'Sweet not found'}, 404)
        return make_response(sweet.to_dict(), 200)
api.add_resource(SweetById, "/sweets/<int:id>")

class VendorSweets(Resource):
    def post(self):
        fields = request.get_json()
        try:
            vendor_sweet = VendorSweet(
                price=fields.get('price'),
                sweet_id=fields.get('sweet_id'),
                vendor_id=fields.get('vendor_id'),
            )
            db.session.add(vendor_sweet)
            db.session.flush()
            vendor_sweet_dict = vendor_sweet.to_dict()
            sweet_obj = Sweet.query.filter_by(id=vendor_sweet.sweet_id).one()
            vendor_obj = Vendor.query.filter_by(id=vendor_sweet.vendor_id).one()
            vendor_sweet_dict['sweet'] = sweet_obj.to_dict()
            vendor_sweet_dict['vendor'] = vendor_obj.to_dict()
            db.session.commit()

            return make_response(vendor_sweet_dict, 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

    def delete(self, id):
        vendor_sweet = VendorSweet.query.filter_by(id=id).one_or_none()
        if vendor_sweet is None:
            return make_response({'error': 'VendorSweet not found'}, 404)
        db.session.delete(vendor_sweet)
        db.session.commit()
        return make_response({}, 204)
api.add_resource(VendorSweets, "/vendor_sweets", "/vendor_sweets/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)