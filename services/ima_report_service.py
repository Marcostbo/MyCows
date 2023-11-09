from datetime import datetime, timedelta
from typing import Optional

from enums.animal import AnimalSex
from models import Animal, User


class IMAReportService:
    base_date: datetime.date = datetime.now().date()  # Base date to create the IMA report
    base_days: int = 365

    @classmethod
    def build_ima_report(cls, public_id: int) -> dict:
        animals = Animal.query.join(User).filter(User.public_id == public_id)
        return {
            'male_00_12': cls.calculate_animal_count(animals, AnimalSex.Male, (0, 1)),
            'female_00_12': cls.calculate_animal_count(animals, AnimalSex.Female, (0, 1)),
            'male_13_24': cls.calculate_animal_count(animals, AnimalSex.Male, (1, 2)),
            'female_13_24': cls.calculate_animal_count(animals, AnimalSex.Female, (1, 2)),
            'male_25_36': cls.calculate_animal_count(animals, AnimalSex.Male, (2, 3)),
            'female_25_36': cls.calculate_animal_count(animals, AnimalSex.Female, (2, 3)),
            'bulls': cls.calculate_animal_count(animals, AnimalSex.Male, (3, None)),
            'cows': cls.calculate_animal_count(animals, AnimalSex.Female, (3, None)),
            'total': animals.count()
        }

    @classmethod
    def calculate_animal_count(cls, animals, sex: AnimalSex, age_range: tuple[int, Optional[int]] = (0, None)) -> int:
        birth_date_filter = Animal.birth_date <= cls.base_date - timedelta(cls.base_days * age_range[0])
        if age_range[1]:
            birth_date_filter &= Animal.birth_date >= cls.base_date - timedelta(cls.base_days * age_range[1])

        return animals.filter(Animal.animal_sex == sex, birth_date_filter).count()
