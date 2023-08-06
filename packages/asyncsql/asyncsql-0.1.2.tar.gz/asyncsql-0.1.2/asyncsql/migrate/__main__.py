import argparse
import asyncio
import sys

from ..backends import sql_backend
from ..helpers import migrate
from ..settings import settings


def parse_args() -> argparse.Namespace:
    """Parse command line options ro run SQL migrations.

    Returns:
        argparse.Namespace -- cli options to take into account
    """
    parser = argparse.ArgumentParser(
        description="Run SQL Migrations", prog="asyncsql.migrate"
    )
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("--sql-dir", "-d", default=settings.sql_dir)
    return parser.parse_args()


async def run_migrate(parsed_args):
    conn = await sql_backend.conn
    for filename in parsed_args.filenames:
        await migrate(conn, filename)
        sys.stdout.write(f"{filename}... ok\n")


if __name__ == "__main__":
    err_found = False
    parsed_args = parse_args()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_migrate(parsed_args))
    except KeyboardInterrupt:
        pass
    except RuntimeError as e:
        err_found = True
        sys.stderr.write(f"Migrate failed!\n{e}\n")
    finally:
        loop.close()

    if err_found:
        sys.exit(1)
