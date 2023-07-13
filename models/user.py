from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime(), nullable=True)
    cows = db.relationship('Cow', backref='owner', lazy=True)

    @property
    def simple_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'date_joined': self.date_joined
        }
