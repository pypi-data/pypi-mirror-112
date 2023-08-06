# AsyncSQL

AsyncSQL aims to provide simple and efficient way to perform PostgreSQL
requests with aiohttp.

## Install

As python library AsyncSQL may be installed as follows:

```bash
(venv)$ pip install asyncsql
```

## Settings

To connect to PostgreSQL common env vars should use.

For example the following values can be used when develop:

```bash
$ export PGHOST=172.19.0.2  # depends on which IP postgres container is using
$ export PGDATABASE=asyncsql
$ export PGUSER=postgres
$ export PGPASSWORD=xxx
```

By default listing data is paginated. The page size can be specify as follows:

```bash
$ export ASYNCSQL_PER_PAGE=25  # default: 50
```

Folder containing .sql files can be specify as follows:

```bash
$ export ASYNCSQL_SQL_DIR=./tests/data  # default: ./sql_files
```

## Migrate

To ease db setup a simple `migrate` command is provided by AsyncSQL.

For example, we can load tests data as follows:

```bash
(venv)$ python -m asyncsql.migrate -d ./tests/data jobs  # file-2 file-3
jobs... ok
```

No magic bullet here, files order matters and idempotency too.

## Usage

Let's perform some queries on our `jobs` test table.

First we need to define a `Model` object to work with in our python code:

```python
from datetime import datetime
from typing import Optional
from uuid import UUID

from asyncsql.models import Model

class Job(Model):
    id: Optional[UUID] = None
    enabled: bool = False
    func: str
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

Then we need a `Queries` instance:

```python
from asyncsql.queries import Queries

jobs_queries = Queries(
    "jobs",
    model_cls=Job,
    order_fields=("name",)
)
```

Let's connect as follows:

```python
import asyncio
from asyncsql.backends import sql_backend

conn = await sql_backend.conn
```

As the db is empty simple `select` should return an empty list and `has_next`
flag to `False`:

```python
await jobs_queries.select(conn)
# ([], False)
```

Let's insert some data:

```python
for x in range(10):
    await jobs_queries.insert(conn, Job(func="ping", name=f"ping-{x}"))
```

We should now have the following data:

```python
[j.name for j in (await jobs_queries.select(conn))[0]]
# ['ping-0',
#  'ping-1',
#  'ping-2',
#  'ping-3',
#  'ping-4',
#  'ping-5',
#  'ping-6',
#  'ping-7',
#  'ping-8',
#  'ping-9']
```

We can limit the result changing the `per_page` value as follows:

```python
jobs_queries.per_page = 3

jobs, has_next = await jobs_queries.select(conn)
[j.name for j in jobs], has_next 
# (['ping-0', 'ping-1', 'ping-2'], True)
```

As we would do in an API, we can get the next page with a `Cursor` object
as follows:

```python
from asyncsql.cursor import Cursor
Cursor(fields=("name",), obj=jobs[-1])
# gASV6wAAAAAAAAAojANhc2OUfZQojAJpZJSMJDRlNTM1YTQ4LWJmMjgtMTFlYi05ZDc3LTAyNDJhYzEzMDAwMpSMB2VuYWJsZWSUiYwEZnVuY5SMBHBpbmeUjARuYW1llIwGcGluZy0ylIwKY3JlYXRlZF9hdJSMCGRhdGV0aW1llIwIZGF0ZXRpbWWUk5RDCgflBRsUDycNJDGUaAqMCHRpbWV6b25llJOUaAqMCXRpbWVkZWx0YZSTlEsASwBLAIeUUpSFlFKUhpRSlIwKdXBkYXRlZF9hdJRoDEMKB+UFGxQPJw0kMZRoFYaUUpR1KX2UdJQu

where, values, _ = jobs_queries.get_where_from_cursor(_)
where, values
# ('name >= $1 AND id != $2', ['ping-2', '4e535a48-bf28-11eb-9d77-0242ac130002'])

jobs, has_next = await jobs_queries.select(conn, values=values, where=where)
[j.name for j in jobs], has_next 
# (['ping-3', 'ping-4', 'ping-5'], True)
```

`Job` object can be use for update too:

```python
job = (await jobs_queries.select(conn, values=("ping-9",), where="name = $1"))[0][0]
job.id, job.name
# ('4e5692d0-bf28-11eb-9d77-0242ac130002', 'ping-9')

job.name = "ping-x"

new_job = await jobs_queries.update(conn, job)
new_job.name
# ping-x
```

Let's clean this demo:

```python
jobs_queries.per_page = 10

for j in (await jobs_queries.select(conn))[0]:
    await jobs_queries.delete_by_id(conn, j.id)
```

## Ideas

- make smaller cursor: serializing the whole object may be an overhead
- work with templated .sql files instead of hard coded `sql` strings in `Queries`

## Contributing

Contribution is welcome. It may be simple but tested as it started.

## License

MIT
