from functools import wraps
from io import BytesIO
from typing import Optional

from aiohttp import ClientSession, ClientResponse, FormData

from .errors import *
from .responses import *

ENDPOINT = "https://pigeonburger.xyz/api/v1/"


def process_resp(resp: ClientResponse) -> None:
    if resp.ok:
        return None
    elif resp.status == 401:
        raise AuthorizationException(resp.reason)
    elif resp.status == 429:
        raise RatelimitException(resp=resp)
    else:
        raise HTTPException(resp.reason, status_code=resp.status)


def require_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.client_session:
            return await func(self, *args, **kwargs)
        else:
            raise NoInitialisedSession

    return wrapper


class AsyncEditVideoBotSession:
    def __init__(
            self,
            authorization: Authorization,
            *,
            client_session: Optional[ClientSession] = None,
    ):
        self._authorization = authorization

        self.client_session = client_session
        self._client_session_is_passed = self.client_session is not None

    async def __aenter__(self):
        if not self._client_session_is_passed:
            self.client_session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._client_session_is_passed:
            await self.client_session.close()

    @classmethod
    def from_api_key(cls, api_key: str, *, client_session: ClientSession = None):
        authorization = Authorization(api_key)
        return cls(authorization, client_session=client_session)

    @property
    def _headers(self):
        return {
            "EVB_AUTH": self._authorization.token
        }

    @require_session
    async def edit(self, input_media: bytes, commands: str, ext: str = "mp4") -> bytes:
        """Edit a file-like object using the /edit/ endpoint.

        :argument input_media Bytes of media to be sent to the API.
        :argument commands A valid EditVideoBot command string.
        :argument ext File extension to use when creating the file to be sent to the API. Default is mp4."""

        form = FormData()

        form.add_field("file", BytesIO(input_media), filename=f"input.{ext}")
        form.add_field("commands", commands)

        async with self.client_session.post(f"{ENDPOINT}edit/", headers=self._headers, data=form) as resp:
            process_resp(resp)

            try:
                response_data = EditResponse.from_json(await resp.json())
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise

        async with self.client_session.get(response_data.media_url) as resp:
            process_resp(resp)

            return await resp.read()

    @require_session
    async def stats(self) -> StatsResponse:
        """Retrieve stats from the /stats/ endpoint."""

        async with self.client_session.get(f"{ENDPOINT}stats/", headers=self._headers) as resp:
            process_resp(resp)

            try:
                return StatsResponse.from_json(await resp.json())
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise


__all___ = ["AsyncEditVideoBotSession"]
