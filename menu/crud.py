from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from menu import models


async def get_all_products(
    db: AsyncSession, skip: int, limit: int
) -> Sequence[models.Product]:
    """
    Retrieves a list of products from the database with pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        Sequence[models.Product]: A list of products.
    """
    query = select(models.Product).offset(skip).limit(limit)
    products_list = await db.execute(query)

    return products_list.scalars().all()


async def get_single_product(db: AsyncSession, product_name: str) -> models.Product:
    """
    Retrieves a single product by name from the database.

    Args:
        db (AsyncSession): The database session.
        product_name (str): The name of the product to retrieve.

    Returns:
        models.Product: The product with the specified name, or None if not found.
    """
    query = select(models.Product).where(models.Product.name == product_name)
    product = await db.execute(query)

    return product.scalar()
