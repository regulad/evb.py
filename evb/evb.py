from io import FileIO
from os.path import basename
from typing import Optional, Iterable

from aiohttp import ClientSession, ClientResponse, FormData

from ._decos import *
from ._endpoint import *
from .commands import *
from .errors import *
from .responses import *


def _process_resp(resp: ClientResponse) -> None:
    if resp.ok:
        return None
    elif resp.status == 401:
        raise AuthorizationException(resp.reason)
    elif resp.status == 429:
        raise RatelimitException(resp=resp)
    else:
        raise HTTPException(resp.reason, status_code=resp.status)


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
    async def edit(self, fp: FileIO, commands: Iterable[Commands]) -> bytes:
        """Edit a file-like object using the /edit/ endpoint.
        Due to an API limitation, the file-lke object must have a name attribute."""

        command_strs = []

        for command in commands:
            command_strs.append(command.__str__())

        command_str = ", ".join(command_strs)

        form = FormData()

        form.add_field("file", fp, filename=basename(fp.name))
        form.add_field("commands", command_str)

        async with self.client_session.post(f"{ENDPOINT}edit/", headers=self._headers, data=form) as resp:
            _process_resp(resp)

            try:
                response_data = EditResponse.from_json(await resp.json())
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise

        async with self.client_session.get(response_data.media_url) as resp:
            _process_resp(resp)

            return await resp.read()

    @require_session
    async def stats(self) -> StatsResponse:
        """Retrieve stats from the /stats/ endpoint."""

        async with self.client_session.get(f"{ENDPOINT}stats/", headers=self._headers) as resp:
            _process_resp(resp)

            try:
                return StatsResponse.from_json(await resp.json())
            except KeyError:
                raise UnknownResponse(resp=resp)
            except Exception:
                raise


__all___ = ["AsyncEditVideoBotSession"]
