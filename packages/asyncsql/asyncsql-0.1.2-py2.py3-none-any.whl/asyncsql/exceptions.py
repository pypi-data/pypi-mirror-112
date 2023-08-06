class AsyncSQLError(Exception):
    pass


class InvalidCursor(AsyncSQLError):
    pass
