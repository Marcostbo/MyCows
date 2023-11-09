from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow_enum import EnumField

from enums.animal import AnimalType, AnimalSex
from schemas.user import UserSchema

from datetime import datetime


class ImaReportSchema(Schema):
    male_00_12 = fields.Integer()
    female_00_12 = fields.Integer()
