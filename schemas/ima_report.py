from marshmallow import Schema, fields


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
