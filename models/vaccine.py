from database import db
from models.base import BaseModel


class Vaccine(BaseModel):
    name = db.Column(db.String(50), nullable=False)
    applications = db.relationship('AnimalVaccination', backref='vaccine')

    def __repr__(self):
        return f'{self.name} Vaccine'
