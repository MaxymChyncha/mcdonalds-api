from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    """
    Base schema for product data.

    Attributes:
        name (str): The name of the product.
        description (Optional[str]): A description of the product.
        calories (Optional[float]): The caloric content of the product.
        fats (Optional[float]): The fat content of the product.
        carbs (Optional[float]): The carbohydrate content of the product.
        proteins (Optional[float]): The protein content of the product.
        unsaturated_fats (Optional[float]): The unsaturated fat content of the product.
        sugar (Optional[float]): The sugar content of the product.
        salt (Optional[float]): The salt content of the product.
        portion (Optional[float]): The portion size of the product.
    """

    name: str
    description: Optional[str]
    calories: Optional[float]
    fats: Optional[float]
    carbs: Optional[float]
    proteins: Optional[float]
    unsaturated_fats: Optional[float]
    sugar: Optional[float]
    salt: Optional[float]
    portion: Optional[float]


class Product(ProductBase):
    """
    Schema for product data including ID.

    Inherits from ProductBase.
    """

    id: int

    class Config:
        from_attributes = True
