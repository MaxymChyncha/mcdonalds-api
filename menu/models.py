from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database.engine import Base


class Product(Base):
    """
    ORM model for the products table.

    Attributes:
        id (int): The primary key of the product.
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

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(63), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    calories: Mapped[float] = mapped_column(Float, nullable=True)
    fats: Mapped[float] = mapped_column(Float, nullable=True)
    carbs: Mapped[float] = mapped_column(Float, nullable=True)
    proteins: Mapped[float] = mapped_column(Float, nullable=True)
    unsaturated_fats: Mapped[float] = mapped_column(Float, nullable=True)
    sugar: Mapped[float] = mapped_column(Float, nullable=True)
    salt: Mapped[float] = mapped_column(Float, nullable=True)
    portion: Mapped[float] = mapped_column(Float, nullable=True)
