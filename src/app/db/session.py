from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import settings

# SQLALCHEMY
engine = create_async_engine(settings.pg_dsn.unicode_string(), pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine)
