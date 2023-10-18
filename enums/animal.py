from enum import Enum


class AnimalType(Enum):
    """
        An enumeration representing the types of animals, including:

        - Cow: Mature female cattle.
        - Bull: Mature male cattle.
        - Heifer: Young female cattle that haven't had a calf.
        - Calf: Young cattle, typically less than one year old.

        This enum is used to categorize and identify the type of animals in a dataset or application.
    """
    Cow = 1
    Bull = 2
    Heifer = 3
    Calf = 4
