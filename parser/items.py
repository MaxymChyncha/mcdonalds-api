from dataclasses import dataclass


@dataclass
class Product:
    """
    Dataclass representing product attributes.

    Attributes:
        name (str): The name of the product.
        description (str): A description of the product.
        calories (float): The caloric content of the product.
        fats (float): The fat content of the product.
        carbs (float): The carbohydrate content of the product.
        proteins (float): The protein content of the product.
        unsaturated_fats (float): The unsaturated fat content of the product.
        sugar (float): The sugar content of the product.
        salt (float): The salt content of the product.
        portion (float): The portion size of the product.
    """

    name: str
    description: str
    calories: float
    fats: float
    carbs: float
    proteins: float
    unsaturated_fats: float
    sugar: float
    salt: float
    portion: float
