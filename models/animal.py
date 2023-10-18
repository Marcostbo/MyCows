from database import db
from models.base import BaseModel
from sqlalchemy import Enum
from enums.animal import AnimalType


class Animal(BaseModel):
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birth_date = db.Column(db.Date)
    origin = db.Column(db.String(120))
    animal_type = db.Column(Enum(AnimalType), nullable=False)

    # Define the parent relationships to the Kinship model
    kinship = db.relationship("Animal", backref="kid", lazy=True)
    mothership = db.relationship("Animal", backref="mother", lazy=True)
    fathership = db.relationship("Animal", backref="father", lazy=True)

    def __repr__(self):
        return f'<Animal {self.name}. Owner {self.owner.name}>'

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.simple_serialize
        }


class Kinship(BaseModel):
    kid_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    father_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
