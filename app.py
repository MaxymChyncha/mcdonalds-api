from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database.initialize import init_db
from menu import router as menu_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for managing the lifespan of a FastAPI application.

    Initializes the database when the application starts.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(menu_router.router)


@app.get("/")
async def index() -> str:
    """
    Endpoint to access the McDonald's API.

    Returns:
        str: A welcome message informing users about the available functionalities.
    """
    message = (
        "Welcome to the McDonald's API! 🍔🍟 "
        "Here you can explore the menu and get detailed information for each item.")
    return message


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
