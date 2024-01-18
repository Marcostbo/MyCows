from marshmallow import Schema, fields

from schemas.animal import AnimalSchema, BaseAnimalSchema


class VaccineSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class AnimalVaccinationCreationSchema(Schema):
    animal_id = fields.String(required=True)
    vaccine_id = fields.String(required=True)
    vaccinated_on = fields.Date(required=False)

    class Meta:
        ordered = False


class AnimalVaccinationSchema(Schema):
    animal = fields.Nested(BaseAnimalSchema())
    vaccine = fields.Nested(VaccineSchema())
    vaccinated_on = fields.Date(required=False)

    class Meta:
        ordered = False
