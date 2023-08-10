from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    vendor_sweets = db.relationship('VendorSweet', backref='sweet')
    
    # TODO Add serialization
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    vendor_sweets = db.relationship('VendorSweet', backref='vendor')
    
    # TODO Add serialization
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    
    # TODO Add serialization
    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
