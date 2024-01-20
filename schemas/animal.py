from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow_enum import EnumField

from enums.animal import AnimalType, AnimalSex
from schemas.user import UserSchema

from datetime import datetime


class BaseAnimalSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    birth_date = fields.Date(format='%Y-%m-%d', required=True)
    age = fields.Integer()
    origin = fields.String()
    animal_type = EnumField(AnimalType)
    animal_sex = EnumField(AnimalSex)

    class Meta:
        ordered = True


class AnimalSchema(BaseAnimalSchema):
    owner = fields.Nested(UserSchema())

    class Meta:
        ordered = True


class CreateAnimalSchema(Schema):
    name = fields.String(required=True)
    birth_date = fields.Date(format='%Y-%m-%d', required=True)
    origin = fields.String()
    animal_type_id = fields.Integer(required=True)
    mother_id = fields.Integer()
    father_id = fields.Integer()

    @validates("name")
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('Email must be more than 3 characters', 'email')

    @validates("animal_type_id")
    def validate_animal_type_id(self, value):
        if value not in {enum.value for enum in AnimalType}:
            raise ValidationError("Invalid animal type ID")

    @validates("birth_date")
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError("Invalid Birhdate. Must not be greater than today")


class UpdateAnimalSchema(Schema):
    name = fields.String()
    birth_date = fields.Date(format='%Y-%m-%d')
    animal_sex = EnumField(AnimalSex)
    animal_type = EnumField(AnimalType)
    origin = fields.String()


class BaseDashboardSchema(Schema):
    type = fields.String()
    count = fields.Integer()


class AnimalQuerySchema(Schema):
    name = fields.String(required=False)
