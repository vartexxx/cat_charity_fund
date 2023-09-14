from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charity_is_enable,
    check_fully_invested, check_charity_project_before_edit,
    check_invested_amount_is_null)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await invest(
        project=new_charity_project,
        crud_class=donation_crud,
        session=session
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_is_enable(
        charity_project_id, session
    )
    await check_fully_invested(charity_project_id, session)
    await check_charity_project_before_edit(
        full_amount=obj_in.full_amount,
        charity_project_id=charity_project_id,
        session=session
    )
    await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_is_enable(
        charity_project_id, session
    )
    await check_invested_amount_is_null(
        charity_project_id, session
    )
    await check_fully_invested(charity_project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
