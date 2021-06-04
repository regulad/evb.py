from functools import wraps

from .errors import NoInitialisedSession


def require_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.client_session:
            return await func(self, *args, **kwargs)

        raise NoInitialisedSession

    return wrapper
