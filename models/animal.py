from database import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
