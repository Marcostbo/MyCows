from database import db
from models.base import BaseModel
from sqlalchemy import Enum
from enums.animal import AnimalType


class Animal(BaseModel):
    """
        Represents an animal in a database.

        Attributes:
            - name (str): The name of the animal.
            - owner_id (int): The ID of the owner (foreign key).
            - birth_date (date): The date of birth of the animal.
            - origin (str): The origin or place of birth of the animal.
            - animal_type (AnimalType): The type of the animal (e.g., 'Cow', 'Bull', 'Heifer', 'Calf').

        Relationships:
            - kinship (list of Animal): Children of this animal (back reference to Kinship model).
            - mothership (list of Animal): Animals that are mothers of this animal (back reference to Kinship model).
            - fathership (list of Animal): Animals that are fathers of this animal (back reference to Kinship model).

        This model represents animals in a database, with fields for their name, owner, birth date, origin, and type.
        The relationships to the Kinship model define parent-child relationships.
        """
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
