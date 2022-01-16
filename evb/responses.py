from datetime import datetime

from aiohttp import ClientSession

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Authorization:
    def __init__(self, token: str):
        self._token = token

    @property
    def token(self):
        return self._token


class EditResponse:
    """Response received from the server when POSTing to /edit"""

    def __init__(
            self,
            error: bool,
            code: int,
            is_video: bool,
            media_url: str,
            media_size: int,
            command_str: str,
            *,
            client: ClientSession,
    ):
        self._error = error
        self._code = code
        self._is_video = is_video
        self._media_url = media_url
        self._media_size = media_size
        self._command_str = command_str
        self._client = client

    @classmethod
    def from_json(cls, json_response: dict, client: ClientSession):
        return cls(
            json_response["error"],
            json_response["code"],
            json_response["is_video"],
            json_response["media_url"],
            json_response["media_size"],
            json_response["command_str"],
            client=client,
        )

    @property
    def error(self):
        return self._error

    @property
    def code(self):
        return self._code

    @property
    def is_video(self):
        return self._is_video

    @property
    def media_url(self):
        return self._media_url

    @property
    def media_size(self):
        return self._media_size

    @property
    def command_str(self):
        return self._command_str

    def __dict__(self):
        return {
            "error": self.error,
            "code": self.code,
            "is_video": self.is_video,
            "media_url": self.media_url,
            "media_size": self.media_size,
            "command_str": self.command_str,
        }

    def __getitem__(self, item):
        return self.__dict__()[item]

    async def download(self) -> bytes:
        """Downloads the media the response refers to."""

        async with self._client.get(self.media_url) as resp:
            return await resp.read()


class StatsResponse:
    """Response received from the server when GETing to /stats"""

    def __init__(
            self,
            error: bool,
            code: int,
            email: str,
            level: str,
            remaining_daily_requests: int,
            videos_edited: int,
            photos_edited: int,
            total_edited: int,
            first_edit: str,
            latest_edit: str,
            favourite_cmd: str,
    ):
        self._error = error
        self._code = code
        self._email = email
        self._level = level
        self._remaining_daily_requests = remaining_daily_requests
        self._videos_edited = videos_edited
        self._photos_edited = photos_edited
        self._total_edited = total_edited
        self._first_edit = first_edit
        self._latest_edit = latest_edit
        self._favourite_cmd = favourite_cmd

    @classmethod
    def from_json(cls, json_response: dict):
        return cls(
            json_response["error"],
            json_response["code"],
            json_response["email"],
            json_response["level"],
            json_response["remaining_daily_requests"],
            json_response["videos_edited"],
            json_response["photos_edited"],
            json_response["total_edited"],
            json_response["first_edit"],
            json_response["latest_edit"],
            json_response["favourite_cmd"],
        )

    @property
    def error(self):
        return self._error

    @property
    def code(self):
        return self._code

    @property
    def email(self):
        return self._email

    @property
    def level(
            self,
    ):  # Should make an Enum of possible values and return an attribute of that Enum
        return self._level

    @property
    def remaining_daily_requests(self):
        return self._remaining_daily_requests

    @property
    def videos_edited(self):
        return self._videos_edited

    @property
    def photos_edited(self):
        return self._photos_edited

    @property
    def total_edited(self):
        return self._total_edited

    @property
    def first_edit(self):
        return datetime.strptime(self._first_edit, DATETIME_FORMAT)

    @property
    def latest_edit(self):
        return datetime.strptime(self._latest_edit, DATETIME_FORMAT)

    @property
    def favourite_cmd(self) -> str:
        return self._favourite_cmd

    def __dict__(self):
        return {
            "error": self.error,
            "code": self.code,
            "email": self.email,
            "level": self.email,
            "remaining_daily_requests": self.remaining_daily_requests,
            "videos_edited": self.videos_edited,
            "photos_edited": self.photos_edited,
            "total_edited": self.total_edited,
            "first_edit": self.first_edit,
            "latest_edit": self.latest_edit,
            "favourite_cmd": self.favourite_cmd,
        }


__all__ = ["Authorization", "EditResponse", "StatsResponse"]
