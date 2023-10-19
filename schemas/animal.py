from marshmallow import Schema, fields, validates, ValidationError
from marshmallow_enum import EnumField

from enums.animal import AnimalType
from schemas.user import UserSchema


class BaseAnimalSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    birth_date = fields.Date(required=True)
    origin = fields.String()
    animal_type = EnumField(AnimalType)

    class Meta:
        ordered = True


class AnimalSchema(BaseAnimalSchema):
    owner = fields.Nested(UserSchema())

    class Meta:
        ordered = True


class CreateAnimalSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    birth_date = fields.Date(required=True)
    origin = fields.String()
    animal_type = fields.Integer(required=True)
    owner = fields.Nested(UserSchema())
    mother_id = fields.Integer()
    father_id = fields.Integer()

    @validates("animal_type")
    def validate_animal_type(self, value):
        if value not in {enum.value for enum in AnimalType}:
            raise ValidationError("Invalid animal type ID")
