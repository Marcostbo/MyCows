from database import db
from models.base import BaseModel


class Vaccine(BaseModel):
    name = db.Column(db.String(50), nullable=False)
