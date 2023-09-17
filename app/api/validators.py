from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект с таким id не найден!'
        )
    return charity_project


async def check_invested_amount(
        charity_project_id: int,
        session: AsyncSession
):
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_full_amount(
        invested_amount: int,
        full_amount_in: int
) -> int:
    if full_amount_in < invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Внесённая сумма должна быть больше новой!'
        )
    return full_amount_in


async def check_project_closed(charity_project_id: int, session: AsyncSession) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
