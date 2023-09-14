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


async def check_charity_is_enable(
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


async def check_charity_project_before_edit(
        charity_project_id: int,
        full_amount: int,
        session: AsyncSession) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if full_amount is not None:
        if charity_project.invested_amount > full_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Внесённая сумма должна быть больше новой!'
            )
        if charity_project.invested_amount == full_amount:
            charity_project.fully_invested = True
        return charity_project


async def check_invested_amount_is_null(
        charity_project_id: int,
        session: AsyncSession
):
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_fully_invested(charity_project_id: int, session: AsyncSession) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
