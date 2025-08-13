from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Engine asíncrono configurado para PgBouncer
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={
        "statement_cache_size": 0  # <--- desactiva prepared statements
    },
)

# Sessionmaker para sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base para modelos
Base = declarative_base()


# Dependencia para rutas
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
