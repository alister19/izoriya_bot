from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

engine = None
_sessionmaker = None

# Инициализация подключения к БД
async def init_db(database_url: str):
    global engine, _sessionmaker

    print(f"Connections to database: {database_url}")

    engine = create_async_engine(database_url, echo=True)
    _sessionmaker = sessionmaker(engine, expire_on_commit=False,
                                 class_=AsyncSession)
    
    # Создание таблиц при первом запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Получить сессию
def get_session() -> AsyncSession:
    if _sessionmaker is None:
        raise RuntimeError("Database not initialized. Call init_db() first")
    return _sessionmaker()