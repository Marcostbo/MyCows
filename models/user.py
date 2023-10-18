from database import db
from models.base import BaseModel


class User(BaseModel):
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    animals = db.relationship('Animal', backref='owner', lazy=True)

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }
