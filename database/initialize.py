import json
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from parser import config
from database.engine import Base, engine
from menu.models import Product


def load_json_data(file_name: str) -> dict:
    """
    Loads JSON data from a file.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        dict: The JSON data from the file.
    """
    file_path = os.path.join(config.FILE_PATH, file_name)
    with open(file_path, "r") as file:
        return json.load(file)


async def update_product(db: AsyncSession, product_data: dict) -> None:
    """
    Updates or creates a product in the database.

    Args:
        db (AsyncSession): The database session.
        product_data (dict): The product data to update or create.
    """
    query = await db.execute(
        select(Product).where(Product.name == product_data.get("name"))
    )

    if product := query.scalar_one_or_none():
        product.description = product_data.get("description")
        product.calories = product_data.get("calories")
        product.fats = product_data.get("fats")
        product.carbs = product_data.get("carbs")
        product.proteins = product_data.get("proteins")
        product.unsaturated_fats = product_data.get("unsaturated_fats")
        product.sugar = product_data.get("sugar")
        product.salt = product_data.get("salt")
        product.portion = product_data.get("portion")
    else:
        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            calories=product_data.get("calories"),
            fats=product_data.get("fats"),
            carbs=product_data.get("carbs"),
            proteins=product_data.get("proteins"),
            unsaturated_fats=product_data.get("unsaturated_fats"),
            sugar=product_data.get("sugar"),
            salt=product_data.get("salt"),
            portion=product_data.get("portion"),
        )

    db.add(product)


async def init_db() -> None:
    """
    Initializes the database by creating all tables and loading initial data.

    This function sets up the database schema and populates it with initial product data
    from a JSON file.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as db:
        products_data = load_json_data(file_name=config.MENU_FILE_NAME)

        for product_data in products_data:
            await update_product(db, product_data)

        await db.commit()
