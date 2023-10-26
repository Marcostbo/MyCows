from database import db
from models.base import BaseModel


class User(BaseModel):
    """
        Represents a user in the application.

        Attributes:
            - public_id (str): A unique public UUID4 identifier for the user.
            - name (str): The name of the user.
            - email (str): The email address of the user (unique).
            - password (str): The password of the user.
            - animals (list of Animal): A list of animals owned by the user.

        This model represents users in the application, with fields for their public ID, name, email, and password.
        The 'animals' relationship represents the animals owned by the user.

        Relationships:
            - animals (list of Animal): A list of animals owned by the user (back reference to the Animal model).
        """
    public_id = db.Column(db.String(50), unique=True, index=True)
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
