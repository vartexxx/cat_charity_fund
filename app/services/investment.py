from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def entry_to_db(obj: Base, session: AsyncSession) -> Base:
    if isinstance(obj, (CharityProject, Donation)):
        await session.commit()
        await session.refresh(obj)
        return obj
    else:
        raise ValueError('Не поддерживаемый тип.')


def close_object(obj: Base) -> None:
    if isinstance(obj, CharityProject):
        obj.fully_invested = (obj.full_amount == obj.invested_amount)
        if obj.fully_invested:
            obj.close_date = datetime.now()


async def invest(
    project: CharityProject,
    crud_class: Base,
    session: AsyncSession
) -> None:
    objects = await crud_class.get_opened_objects(
        session=session
    )
    for obj in objects:
        needed = project.full_amount - project.invested_amount
        if not needed:
            break
        available = obj.full_amount - obj.invested_amount
        to_add = min(needed, available)
        obj.invested_amount += to_add
        project.invested_amount += to_add
        close_object(obj)
    close_object(project)

    await entry_to_db(
        obj=project,
        session=session
    )
