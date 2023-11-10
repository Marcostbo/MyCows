from enums.animal import AnimalType
from models import Animal


class AnimalService:

    @classmethod
    def check_permission(cls, animal: Animal, public_id: str) -> bool:
        return animal.owner.public_id == public_id

    @classmethod
    def get_animal_type_by_id(cls, type_id: int) -> AnimalType:
        if type_id == 1:
            return AnimalType.Cow
        elif type_id == 2:
            return AnimalType.Bull
        elif type_id == 3:
            return AnimalType.Heifer
        elif type_id == 4:
            return AnimalType.Calf
        else:
            # Handle the case where the input value is not valid
            raise ValueError("Invalid input value")
