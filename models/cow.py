from database import db


class Cow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner.simple_serialize
        }

# class Bull(db.Model):
#     a = 1
#
#
# class Calf(db.Model):
#     a = 1
