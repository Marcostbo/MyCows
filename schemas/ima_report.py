from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow_enum import EnumField

from enums.animal import AnimalType, AnimalSex
from schemas.user import UserSchema

from datetime import datetime


class ImaReportSchema(Schema):
    male_00_12 = fields.Integer()
    female_00_12 = fields.Integer()
    male_13_24 = fields.Integer()
    female_13_24 = fields.Integer()
    male_25_36 = fields.Integer()
    female_25_36 = fields.Integer()
    bulls = fields.Integer()
    cows = fields.Integer()
    total = fields.Integer()
