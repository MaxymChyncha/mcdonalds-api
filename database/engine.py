from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./mcdonalds_products.db"


engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models with async attributes.

    Combines `AsyncAttrs` for asynchronous attribute handling
    and `DeclarativeBase` for declarative ORM definitions.

    Example:
        class User(Base):
            __tablename__ = 'users'

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String, nullable=False)
            email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    """

    __abstract__ = True


async def get_db() -> None:
    """
    Provides an async database session generator.

    Yields:
        An asynchronous database session.
    """
    async with async_session() as session:
        yield session
        await session.commit()
