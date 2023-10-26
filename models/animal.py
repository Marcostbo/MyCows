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

        This model represents animals in a database, with fields for their name, owner, birth date, origin, and type.
        The relationships to the Kinship model define parent-child relationships.
        """
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    origin = db.Column(db.String(120))
    animal_type = db.Column(Enum(AnimalType), nullable=False)

    # Define the Owner relationship with table User
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the parent relationships:
    father_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

    # Create relationships for "father" and "mother"
    father = db.relationship("Animal", remote_side='Animal.id', backref="fathership", foreign_keys=[father_id])
    mother = db.relationship("Animal", remote_side='Animal.id', backref="mothership", foreign_keys=[mother_id])

    def __repr__(self):
        return f'<Animal {self.name}. Owner {self.owner.name}>'
