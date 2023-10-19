from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow_enum import EnumField

from enums.animal import AnimalType
from schemas.user import UserSchema

from datetime import datetime


class BaseAnimalSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    birth_date = fields.Date(format='%Y-%m-%d', required=True)
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
    birth_date = fields.Date(format='%Y-%m-%d', required=True)
    origin = fields.String()
    animal_type = fields.Integer(required=True)
    mother_id = fields.Integer()
    father_id = fields.Integer()

    @validates("name")
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('Email must be more than 3 characters', 'email')

    @validates("animal_type")
    def validate_animal_type(self, value):
        if value not in {enum.value for enum in AnimalType}:
            raise ValidationError("Invalid animal type ID")

    @validates("birth_date")
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError("Invalid Birhdate. Must not be greater than today")
