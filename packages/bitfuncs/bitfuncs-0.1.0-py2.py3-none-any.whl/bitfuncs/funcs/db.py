from functools import partial, wraps

from asyncsql.backends import sql_backend
from asyncsql.cursor import Cursor
from chamallow import flow

from ..queries import queries_registry


async def _select_values(queries_name, symbol, limit=None, resolution="P1D"):
    conn = await sql_backend.conn

    cursor_cls = partial(
        Cursor,
        direction="desc",
        fields=("time",),
        query_params={
            "symbol": symbol,
            "resolution": resolution,
        },
    )
    queries = queries_registry[queries_name]

    _w = f"symbol = '{symbol}' AND resolution = '{resolution}'"
    _v = ()

    has_next = True
    values = []

    while has_next and (not limit or len(values) < limit):
        # TODO: use queries.registry
        rows, has_next = await queries.select(
            conn,
            limit=limit,
            values=_v,
            where=_w,
        )
        if not rows:
            break
        values += [r.dict() for r in rows]
        # where, values for the next select
        _w, _v, _ = queries.get_where_from_cursor(cursor_cls(obj=rows[-1]))
    return values


select_values = flow()(_select_values)


def with_last_time():
    def with_last_time_decorator(func):
        @wraps(func)
        async def func_wrapper(queries_name, symbol, *a, resolution="P1D"):
            res = await _select_values(
                queries_name, symbol, limit=1, resolution=resolution
            )
            last_time = res and res[0]["time"]
            return await func(
                last_time, queries_name, symbol, *a, resolution=resolution
            )

        return func_wrapper

    return with_last_time_decorator


@flow()
@with_last_time()
async def insert_values(last_time, queries_name, symbol, values, resolution="P1D"):
    pool = await sql_backend.pool
    inserted = 0
    queries = queries_registry[queries_name]
    async with pool.acquire() as conn:
        for val in values:
            obj = queries.model_cls(symbol=symbol, resolution=resolution, **val)
            if last_time and obj.time <= last_time:
                continue
            await queries.insert(conn, obj)
            inserted += 1
    return inserted or True
