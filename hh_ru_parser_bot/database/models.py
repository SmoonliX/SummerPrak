from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import  AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    experience: Mapped[str] = mapped_column(String(255))
    last_job: Mapped[str] = mapped_column(String(255))
    last_job_date: Mapped[str] = mapped_column(String(255))

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    experience: Mapped[str] = mapped_column(String(255))
    company: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)