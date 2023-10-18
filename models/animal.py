from database import db
from models.base import BaseModel


class Animal(BaseModel):
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birth_date = db.Column(db.Date)
    origin = db.Column(db.String(120))

    def __repr__(self):
        return f'<Animal {self.name} from owner {self.owner.name}>'

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.simple_serialize
        }
