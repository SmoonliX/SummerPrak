from database.models import async_session
from database.models import User, Resume,Vacancy
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def add_resume(title: str, link: str, age: int, experience: str, last_job: str, last_job_date: str) -> None:
    async with async_session() as session:
        resume = Resume(
            title=title,
            link=link,
            age=age,
            experience=experience,
            last_job=last_job,
            last_job_date=last_job_date
        )
        session.add(resume)
        await session.commit()


async def add_vacancy(title: str, experience: str, company: str, city: str) -> None:
    async with async_session() as session:
        resume = Vacancy(
            title=title,
            experience=experience,
            company=company,
            city=city
        )
        session.add(resume)
        await session.commit()
