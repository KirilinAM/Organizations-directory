from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import func
from config import settings
from datetime import datetime

DATABASE_URL = settings.getAsyncDbUrl()

engine = create_async_engine(url=DATABASE_URL)
asyncSessionMaker = async_sessionmaker(engine,expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_ay: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
    
    def toDict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return str(self.toDict())

    
class BaseWithId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
