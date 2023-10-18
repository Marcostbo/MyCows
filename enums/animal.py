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


class AnimalStatus(Enum):
    """
    Enumeration representing the status of an animal.

    Attributes:
        - Alive (int): The animal is currently alive.
        - Dead (int): The animal is deceased.
        - Sold (int): The animal has been sold.

    This enum is used to categorize and identify the current status of animals in a dataset or application.
    """
    Alive = 1
    Dead = 2
    Sold = 3
