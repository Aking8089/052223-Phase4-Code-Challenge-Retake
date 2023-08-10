from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship(
        'HeroPower', backref='hero', cascade='all, delete-orphan')
    powers = association_proxy('hero_powers', 'power',
                               creator=lambda pwr: HeroPower(power=pwr))

    # add serialization rules
    serialize_rules = ('-powers.heroes', '-hero_powers.hero')

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship(
        'HeroPower', backref='power', cascade='all, delete-orphan')
    heroes = association_proxy('hero_powers', 'hero',
                               creator=lambda hr: HeroPower(hero=hr))

    # add serialization rules
    seralize_rules = ('-heroes.powers', '-hero_powers.power')

    # add validation
    @validates('description')
    def validate_description(self, key, description):
        if isinstance(description, str) and len(description) >= 20:
            return description
        raise ValueError("Description must be string of 20+ characters.")

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # add serialization rules
    serialize_rules = ('-power.hero_powers', '-hero.hero_powers')

    # add validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength in ('Strong', 'Weak', 'Average'):
            return strength
        raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'.")

    def __repr__(self):
        return f'<HeroPower {self.id}>'
