from functools import wraps
from io import BytesIO
from typing import Optional, cast, Callable, Coroutine, TypeVar

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

from aiohttp import ClientSession, FormData, ClientResponse

from .responses import *
from .errors import *

_R = TypeVar("_R")
_T = TypeVar("_T")
_C = TypeVar("_C")

_P = ParamSpec("_P")


# I would have made this a static method if I could.
def _require_session(
        func: Callable[[_P], Coroutine[_R, _T, _C]]
) -> Callable[[_P], Coroutine[_R, _T, _C]]:
    """Annotates that a wrapped coroutine function requires an unclosed ClientSession"""

    @wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        self: AsyncEditVideoBotSession = cast(AsyncEditVideoBotSession, args[0])

        if self._client_session is not None and not self._client_session.closed:
            return func(*args, **kwargs)
        else:
            raise NoInitialisedSession(
                f"The {self.__class__.__name__} is unable to find a ClientSession to communicate with. "
                f"One is created on instantiation and is closed when exiting using the object as a context manager."
            )

    return wrapper


class AsyncEditVideoBotSession:
    @staticmethod
    def _process_resp(resp: ClientResponse) -> None:
        if resp.ok:
            return None
        elif resp.status == 401:
            raise AuthorizationException(resp.reason)
        elif resp.status == 429:
            raise RatelimitException(resp=resp)
        else:
            raise HTTPException(resp.reason, status_code=resp.status)

    _ENDPOINT = "https://pigeonburger.xyz/api/v1/"

    def __init__(
            self,
            authorization: Authorization,
            *,
            client_session: Optional[ClientSession] = None,
    ) -> None:
        self._authorization = authorization
        self._client_session: Optional[ClientSession] = client_session

    @property
    def closed(self) -> bool:
        return self._client_session.closed

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def open(self, client_session: Optional[ClientSession] = None) -> None:
        self._client_session = client_session or self._client_session or ClientSession()

    async def close(self) -> None:
        """Closes the connection."""

        return await self._client_session.close()

    @classmethod
    def from_api_key(cls, api_key: str):
        authorization: Authorization = Authorization(api_key)
        return cls(authorization)

    @property
    def _headers(self) -> dict:
        return {"EVB_AUTH": self._authorization.token}

    @_require_session
    async def edit(
            self, input_media: bytes, commands: str, ext: str = "mp4"
    ) -> EditResponse:
        """Edit a file-like object using the /edit/ endpoint.

        :argument input_media Bytes of media to be sent to the API.
        :argument commands A valid EditVideoBot command string.
        :argument ext File extension to use when creating the file to be sent to the API. Default is mp4."""

        form = FormData()

        form.add_field("file", BytesIO(input_media), filename=f"input.{ext}")
        form.add_field("commands", commands)

        async with self._client_session.post(
                f"{self._ENDPOINT}edit/", data=form, headers=self._headers
        ) as resp:
            self._process_resp(resp)

            try:
                return EditResponse.from_json(
                    await resp.json(), client=self._client_session
                )
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise

    @_require_session
    async def stats(self) -> StatsResponse:
        """Retrieve stats from the /stats/ endpoint."""

        async with self._client_session.get(f"{self._ENDPOINT}stats/", headers=self._headers) as resp:
            self._process_resp(resp)

            try:
                return StatsResponse.from_json(await resp.json())
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise


__all___ = ["AsyncEditVideoBotSession"]
