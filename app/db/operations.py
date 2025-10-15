from sqlalchemy import select, delete

from app.db.database import async_session
from app.db.models import User, Task


async def set_user(tg_id) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_tasks(tg_id) -> list[Task]:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        tasks = await session.scalars(select(Task).where(Task.user == user.id))
        return tasks

async def set_task(tg_id, task) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Task(task=task, user=user.id))
        await session.commit()

async def del_task(task_id) -> None:
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.id == task_id))
        await session.commit()