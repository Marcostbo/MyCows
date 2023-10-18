from datetime import datetime
from functools import partial
from pytz import timezone
from database import db


class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=partial(datetime.now, tz=timezone("America/Sao_Paulo")),)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        for field, value in kwargs.items():
            try:
                setattr(self, field, value)
            except AttributeError:
                pass

        self.updated_at = datetime.now()
        db.session.commit()
        return self

    @classmethod
    def get(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).all()
