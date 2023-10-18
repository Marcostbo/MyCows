from database import db
from models.base import BaseModel


class Animal(BaseModel):
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # register_date
    # birth_date

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.simple_serialize
        }
