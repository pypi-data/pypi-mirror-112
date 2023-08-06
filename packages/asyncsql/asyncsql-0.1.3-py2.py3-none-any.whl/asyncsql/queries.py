import itertools
from collections.abc import Iterator
from typing import Tuple
from uuid import UUID

import orjson
from asyncpg.connection import Connection

from .cursor import Cursor
from .exceptions import InvalidCursor
from .helpers import orjson_dumps
from .models import Model
from .settings import settings


class Queries:
    def __init__(
        self,
        table: str,
        cursor_fields: list = (),
        direction: str = "asc",
        id_field: str = "id",
        model_cls: Model = None,
        order_fields: list = (),
        per_page: int = settings.per_page,
        readonly_fields: list = (),
        returning_fields: list = (),
    ) -> None:
        self.cursor_fields = cursor_fields or order_fields
        self.direction = direction
        self.id_field = id_field
        self.model_cls = model_cls
        self.order_fields = order_fields
        self.per_page = per_page
        self.readonly_fields = readonly_fields
        self.returning_fields = returning_fields or [self.id_field]
        self.table = table

    async def delete_by_id(self, conn: Connection, id: UUID) -> Model:
        exists = await self.exists_by_id(conn, id)
        if not exists:
            return
        sql = self.get_delete_by_id_sql()
        await conn.fetchrow(sql, id)
        return True

    async def exists_by_id(self, conn: Connection, id: UUID) -> bool:
        sql = self.get_exists_by_id_sql()
        return bool(await conn.fetchval(sql, id))

    def get_delete_by_id_sql(self):
        return f"DELETE FROM {self.table} WHERE id = $1"

    def get_exists_by_id_sql(self) -> str:
        return f"SELECT 1 FROM {self.table} WHERE id = $1"

    def get_cleaned_data(self, model: Model, create: bool = False) -> dict:
        exclude_fields = list(self.readonly_fields)[:]
        if not create:
            exclude_fields.append(self.id_field)
        return {
            k: v
            for k, v in model.dict(exclude_unset=True).items()
            if k not in exclude_fields
        }

    def get_insert_sql(self, model: Model) -> Tuple[str, list]:
        cleaned_data = self.get_cleaned_data(model, create=True)
        columns = ", ".join(cleaned_data.keys())
        indexes = ", ".join(f"${i}" for i, _ in enumerate(cleaned_data, start=1))
        returning_fields_str = ", ".join(self.returning_fields)
        sql = f"""
INSERT INTO {self.table}({columns})
VALUES({indexes})
RETURNING {returning_fields_str}
""".strip()
        values = [
            v if not v or not model.is_type_dict(k) else orjson_dumps(v)
            for k, v in cleaned_data.items()
        ]
        return sql, values

    def get_order_by(self, direction: str = None, order_fields: list = ()) -> (str):
        return ", ".join(
            f"{f} {direction or self.direction}"
            for f in (order_fields or self.order_fields or [self.id_field])
            if f in self.model_cls.__fields__
        )

    def get_select_by_id_sql(self):
        return f"SELECT * FROM {self.table} WHERE id = $1"

    def get_select_json_sql(
        self, limit: int = None, order_by: str = "", where: str = None
    ):
        last_fields = ", ".join(sorted(set([self.id_field] + list(self.cursor_fields))))
        limit = limit or self.per_page
        order_by = order_by or self.get_order_by()
        return f"""
WITH rows AS (
  SELECT
    *
  FROM {self.table}
  WHERE
    {where or "TRUE"}
  ORDER BY
    {order_by}
  LIMIT {limit + 1}
), has_next AS (
    SELECT true
      FROM rows
    OFFSET {limit}
     LIMIT 1
), ordered_rows AS (
  SELECT
    *
  FROM rows
  LIMIT {limit}
), last_row AS (
    SELECT
      {last_fields}
    FROM rows
    WHERE (SELECT TRUE FROM has_next)
    OFFSET {limit - 1}
    LIMIT 1
)
SELECT
  coalesce(json_agg(ordered_rows)::text, '[]') as rows_to_json,
  (SELECT to_json(last_row) FROM last_row) as last
FROM ordered_rows
""".strip()

    def get_select_json_by_id_sql(self) -> str:
        return f"""
WITH _row AS (
  SELECT
    *
  FROM {self.table}
  WHERE
    id = $1
)
SELECT
  row_to_json(_row)::text
FROM _row
""".strip()

    def get_select_sql(self, limit: int = None, order_by: str = "", where: str = None):
        limit = limit or self.per_page
        order_by = order_by or self.get_order_by()
        return f"""
WITH rows AS (
  SELECT
    *
  FROM {self.table}
  WHERE
    {where or "TRUE"}
  ORDER BY
    {order_by}
  LIMIT {limit + 1}
), has_next AS (
    SELECT true
      FROM rows
    OFFSET {limit}
     LIMIT 1
), ordered_rows AS (
  SELECT
    *
  FROM rows
  LIMIT {limit}
)
SELECT
  *,
  (SELECT * FROM has_next) as has_next
FROM ordered_rows
""".strip()

    def get_update_sql(self, model: Model) -> str:
        cleaned_data = self.get_cleaned_data(model)
        columns = ",\n  ".join(
            f"{k} = ${i}" for i, k in enumerate(cleaned_data.keys(), start=2)
        )
        returning_fields_str = ", ".join(self.returning_fields)
        sql = f"""
UPDATE {self.table}
SET
  {columns}
WHERE
  {self.id_field} = $1
RETURNING {returning_fields_str}
""".strip()
        values = [
            getattr(model, self.id_field),
        ]
        values += [
            v if not v or not model.is_type_dict(k) else orjson_dumps(v)
            for k, v in cleaned_data.items()
        ]
        return sql, values

    def _get_conditions(
        self,
        query_params: dict,
        index: Iterator,
        exclude: list = (),
        only: list = (),
        operator: str = "=",
    ) -> Tuple[list, list]:
        conditions = []
        values = []
        for f in sorted(
            filter(
                lambda x: not only or x in only, set(query_params.keys()) - set(exclude)
            )
        ):
            v = query_params.get(f)
            # nothing to filter on
            if not v or isinstance(v, bool):
                continue
            conditions.append(f"{f} {operator} ${next(index)}")
            values.append(v)
        return conditions, values

    def get_where(
        self,
        cursor_fields: list = (),
        direction: str = "asc",
        last_dict: dict = None,
        or_fields: list = (),
        query_params: dict = None,
        start: int = 1,
    ) -> Tuple[str, list, int]:
        index = itertools.count(start=start)
        operator = ">=" if direction.lower() == "asc" else "<="

        if last_dict:
            only = cursor_fields or self.cursor_fields
            cursor_conditions, cursor_values = self._get_conditions(
                last_dict,
                index,
                exclude=("id",),
                only=only,
                operator=operator,
            )
            cursor_conditions.append(f"id != ${next(index)}")
            cursor_values.append(last_dict["id"])
        else:
            cursor_conditions, cursor_values = [], []

        if query_params:
            and_conditions, and_values = self._get_conditions(
                query_params, index, exclude=or_fields
            )
        else:
            and_conditions, and_values = [], []

        if query_params and or_fields:
            or_conditions, or_values = self._get_conditions(
                query_params, index, only=or_fields
            )
        else:
            or_conditions, or_values = [], []

        if or_conditions:
            and_conditions.append("({})".format(" OR ".join(or_conditions)))

        if cursor_conditions or and_conditions:
            where_query = " AND ".join(cursor_conditions + and_conditions)
        else:
            where_query = ""

        return where_query, cursor_values + and_values + or_values, next(index)

    def get_where_from_cursor(
        self, cursor: object = "", start: int = 1
    ) -> Tuple[str, list, int]:
        if isinstance(cursor, str):
            cursor = Cursor.from_str(self.model_cls, cursor=cursor)
        elif cursor and not isinstance(cursor, Cursor):
            raise InvalidCursor
        return self.get_where(
            cursor_fields=cursor.fields,
            direction=cursor.direction,
            last_dict=cursor.obj_dict,
            or_fields=cursor.or_fields,
            query_params=cursor.query_params,
            start=start,
        )

    async def insert(self, conn: Connection, model: Model):
        sql, values = self.get_insert_sql(model)
        row = await conn.fetchrow(sql, *values)
        return self.model_cls(**{**model.dict(), **dict(row.items())})

    async def select_by_id(self, conn: Connection, id: UUID) -> Model:
        sql = self.get_select_by_id_sql()
        record = await conn.fetchrow(sql, id)
        return record and self.model_cls.from_record(record)

    async def select(
        self,
        conn: Connection,
        limit: int = None,
        order_by: str = "",
        values: list = (),
        where: str = "",
    ) -> Tuple[Model, bool]:
        sql = self.get_select_sql(limit=limit, order_by=order_by, where=where)
        records = await conn.fetch(sql, *values)
        rows = [self.model_cls.from_record(r) for r in records]
        has_next = True if records and records[0]["has_next"] else False
        return rows, has_next

    async def select_json(
        self,
        conn: Connection,
        limit: int = None,
        order_by: str = "",
        values: list = (),
        where: str = "",
    ) -> str:
        sql = self.get_select_json_sql(limit=limit, order_by=order_by, where=where)
        record = await conn.fetchrow(sql, *values)
        return record["rows_to_json"], record["last"] and orjson.loads(record["last"])

    async def select_json_by_id(self, conn: Connection, id: UUID) -> str:
        sql = self.get_select_json_by_id_sql()
        record = await conn.fetchrow(sql, id)
        return record and record["row_to_json"]

    async def update(self, conn: Connection, model: Model) -> UUID:
        sql, values = self.get_update_sql(model)
        row = await conn.fetchrow(sql, *values)
        if not row:
            return
        return self.model_cls(**{**model.dict(), **dict(row.items())})
