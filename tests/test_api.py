import unittest
import evb
import os


class TestStatsResponse(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._session = evb.AsyncEditVideoBotSession.from_api_key(
            os.environ.get("TEST_API_KEY")
        )

    async def asyncSetUp(self) -> None:
        await self._session.open()

    async def runTest(self):
        await self._session.stats()

    async def asyncTearDown(self) -> None:
        await self._session.close()


if __name__ == "__main__":
    unittest.main()
