from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_project_exists, check_invested_amount,
    check_full_amount, check_project_closed)
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
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
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
    project = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    session.add_all(
        invest(
            project,
            await donation_crud.get_opened_objects(session)
        )
    )
    await session.commit()
    await session.refresh(project)
    return project


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
    project = await check_project_exists(
        charity_project_id, session
    )
    if obj_in.full_amount is not None:
        check_full_amount(project.invested_amount, obj_in.full_amount)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_project_closed(charity_project_id, session)
    project = await charity_project_crud.update(
        project, obj_in, session, commit=False
    )
    session.add_all([
        project,
        *invest(
            project,
            await donation_crud.get_opened_objects(session)
        )
    ])
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exists(
        charity_project_id, session
    )
    await check_invested_amount(charity_project_id, session)
    await check_project_closed(charity_project_id, session)
    return await charity_project_crud.remove(charity_project, session)
