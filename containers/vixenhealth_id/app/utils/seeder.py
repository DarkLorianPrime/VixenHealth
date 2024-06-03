import subprocess
from collections import defaultdict
from typing import Dict, List, Any, Type, DefaultDict, Callable

import yaml.parser
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import mapperlib
from sqlalchemy import Insert, select, UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert
from yaml import load, Loader

from config.settings import settings
from storages.database.models import Base
from storages.database.repositories.account import hasher

unique_ids: Dict[str, UUID] = {}


class HashPassword:
    def __call__(self, password):
        return hasher.hash(password, salt=settings.PROJECT_SECRET_KEY.encode())


functions: Dict[str, Callable] = {"HashPassword": HashPassword()}


async def check_fields_on_function(fields: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in fields.items():
        if isinstance(value, dict):
            function_name = value["function"]
            fields[key] = functions[function_name](value["data"])


async def check_fields_on_depends(fields: Dict[str, Any]) -> Dict[str, Any]:
    deps_fields: DefaultDict[str, List[UUID | None]] = defaultdict(list)
    deps_names: List[str] = []
    for key, value in fields.items():
        if not isinstance(value, dict):
            continue

        depends = value.pop("depends", [])
        if not depends:
            continue
        deps_fields[key].extend(
            unique_ids.get(v) for v in depends if unique_ids.get(v) is not None
        )

        deps_names.append(key)

    for deps_name in deps_names:
        fields.pop(deps_name, None)

    return deps_fields


async def insert_row(
    session: AsyncSession, table: Type[Base], fields: Dict[str, Any]
) -> UUID | None:
    stmt: Insert | ReturningInsert = (
        insert(table)
        .values(**fields)
        .on_conflict_do_nothing(
            index_elements=[
                getattr(table, column_name, None)
                for column_name, column_values in fields.items()
                if column_values and isinstance(column_values, str)
            ]
        )
        .returning(table.id)
    )
    try:
        result = await session.execute(stmt)
    except ProgrammingError:
        subprocess.run(["alembic", "upgrade", "head"])
        raise Exception("Process call alembic upgrade, please restart seeder.")

    scalar = result.scalar()

    return scalar


async def get_row(session: AsyncSession, table: Type[Base], row_id: UUID):
    stmt = select(table).where(table.id == row_id)
    result = await session.execute(stmt)
    return result.scalar()


async def create_row(table: Type[Base], session: AsyncSession, **fields):
    unique_id: str | None = fields.pop("unique_id", None)

    deps = await check_fields_on_depends(fields)
    await check_fields_on_function(fields)
    return_id = await insert_row(session, table, fields)
    if return_id is None:
        return

    created_field = await get_row(session, table, return_id)

    if unique_id is not None:
        unique_ids[unique_id] = created_field

    if deps:
        for dependency_name, dependency_value in deps.items():
            depends_field = getattr(created_field, dependency_name)
            if depends_field is None:
                continue

            depends_field.extend(dependency_value)


async def process_row(
    table: Type[Base], rows: List[Dict[str, Any]], session: AsyncSession
):
    for row in rows:
        await create_row(table, session, **row)


async def run_seeder(file: str, session: AsyncSession):
    with open(file, "rb") as f:
        tables = load(f, Loader=Loader)

    if not isinstance(tables, list):
        raise yaml.parser.ParserError(
            "Invalid YAML configuration. Expected a list with objects with `table` and `data`"
        )
    models = return_declared_models()
    for table_seeder in tables:
        table_name = table_seeder["table"]

        table: Type[Base] | None = models.get(table_name, None)
        if table is None:
            raise yaml.parser.ParserError("Couldn't find table '%s'" % table_name)

        await process_row(table, table_seeder["data"], session)

    await session.commit()


def return_declared_models() -> Dict[str, Type[Base]]:
    return {
        mapper.mapped_table.name: mapper.class_
        for registred_mappers in mapperlib._mapper_registries.items()
        for mapper in registred_mappers[0].mappers
    }
