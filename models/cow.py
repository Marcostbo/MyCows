from database import db


class Cow(db.Model):
    owner = db.relationship('User')


class Bull(db.Model):
    a = 1


class Calf(db.Model):
    a = 1
