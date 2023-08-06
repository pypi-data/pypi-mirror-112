from functools import cached_property

from dynaconf import LazySettings


class Settings:
    def __init__(self):
        self._settings = LazySettings(
            ENVVAR_FOR_DYNACONF="ASYNCSQL_SETTINGS",
            ENVVAR_PREFIX_FOR_DYNACONF="ASYNCSQL",
        )

    @cached_property
    def per_page(self):
        return self._settings.get("PER_PAGE", cast="@int", default=50)

    @cached_property
    def sql_dir(self):
        return self._settings.get("SQL_DIR", default="./sql_files")


settings = Settings()
