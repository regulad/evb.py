import os
import unittest

import importlib_resources

import evb


class TestStatsResponse(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._session: evb.AsyncEditVideoBotSession = evb.AsyncEditVideoBotSession.from_api_key(
            os.environ.get("TEST_API_KEY"))

    async def asyncSetUp(self) -> None:
        await self._session.open()

    async def runTest(self):
        stats_response: evb.StatsResponse = await self._session.stats()
        assert stats_response is not None

    async def asyncTearDown(self) -> None:
        await self._session.close()


class TestEditResponse(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._session: evb.AsyncEditVideoBotSession = evb.AsyncEditVideoBotSession.from_api_key(
            os.environ.get("TEST_API_KEY"))
        self._video_data: bytes = importlib_resources.files("evb.tests.data").joinpath("carlos.mp4").read_bytes()

    async def asyncSetUp(self) -> None:
        await self._session.open()

    async def runTest(self):
        edit_response: evb.EditResponse = await self._session.edit(self._video_data, "cap=cap")
        assert edit_response is not None

    async def asyncTearDown(self) -> None:
        await self._session.close()


if __name__ == "__main__":
    unittest.main()
