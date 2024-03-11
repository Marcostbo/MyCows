from database import db
from models.base import BaseModel
from sqlalchemy import Enum
from enums.animal import AnimalType, AnimalSex
from datetime import datetime


class AnimalVaccination(BaseModel):
    __tablename__ = 'animal_vaccination'

    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    vaccinated_on = db.Column(db.Date)

    def __repr__(self):
        return f'Vaccination of {self.vaccine.name} on {self.animal.name} - {self.vaccinated_on}'


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
    animal_type = db.Column(Enum(AnimalType), nullable=True)
    animal_sex = db.Column(Enum(AnimalSex), nullable=True)

    # Define the Owner relationship with table User
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the Vaccinations relationship (Many-to-Many)
    vaccines = db.relationship('Vaccine', secondary='animal_vaccination', backref="animals")
    vaccinations = db.relationship('AnimalVaccination', backref='animal')

    # Define the parent relationships:
    father_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    mother_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

    # Create relationships for "father" and "mother"
    father = db.relationship("Animal", remote_side='Animal.id', backref="fathership", foreign_keys=[father_id])
    mother = db.relationship("Animal", remote_side='Animal.id', backref="mothership", foreign_keys=[mother_id])

    def __repr__(self):
        return f'<Animal {self.name}. Owner {self.owner.name}>'

    @property
    def age(self) -> int:
        return int((datetime.now().date() - self.birth_date).days/30)
