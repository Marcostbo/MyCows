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
    Vaca = 1
    Boi = 2
    Novilha = 3
    Bezerro = 4


class AnimalSex(Enum):
    """
        An enumeration representing the types of animal sex, including:

        - Male: Male animal.
        - Female: Female animal.

        This enum is used to categorize and identify the type of animals in a dataset or application.
    """
    Macho = 1
    Femea = 2


class AnimalStatus(Enum):
    """
    Enumeration representing the status of an animal.

    Attributes:
        - Alive (int): The animal is currently alive.
        - Dead (int): The animal is deceased.
        - Sold (int): The animal has been sold.

    This enum is used to categorize and identify the current status of animals in a dataset or application.
    """
    Vivo = 1
    Morto = 2
    Vendido = 3
