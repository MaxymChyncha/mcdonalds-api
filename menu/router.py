from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_db
from menu import schemas
from menu.crud import get_all_products, get_single_product

router = APIRouter()


@router.get("/all_products/", response_model=list[schemas.Product])
async def read_products(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.Product]:
    """
    Retrieves a paginated list of products.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (AsyncSession, optional): Database session dependency.

    Returns:
        Sequence[schemas.Product]: A list of product schemas.
    """
    return await get_all_products(db=db, skip=skip, limit=limit)


@router.get("/product/{product_name}/", response_model=schemas.Product)
async def read_single_product(
    product_name: str, db: AsyncSession = Depends(get_db)
) -> schemas.Product:
    """
    Retrieves a single product by name.

    Args:
        product_name (str): The name of the product to retrieve.
        db (AsyncSession, optional): Database session dependency.

    Returns:
        schemas.Product: The product schema.

    Raises:
        HTTPException: If the product is not found.
    """
    if product := await get_single_product(db=db, product_name=product_name):
        return product

    raise HTTPException(status_code=404, detail="Product not found")


@router.get("/product/{product_name}/{product_field}/")
async def read_single_product_field(
    product_name: str, product_field: str, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Retrieves a specific field of a single product by name.

    Args:
        product_name (str): The name of the product to retrieve.
        product_field (str): The field of the product to retrieve.
        db (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary containing the requested field and its value.

    Raises:
        HTTPException: If the product or the field is not found.
    """
    if product := await get_single_product(db=db, product_name=product_name):
        if hasattr(product, product_field):
            return {product_field: getattr(product, product_field)}
        raise HTTPException(status_code=404, detail="Field not found")
    raise HTTPException(status_code=404, detail="Product not found")
