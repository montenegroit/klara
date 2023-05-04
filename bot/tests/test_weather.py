import unittest
import asyncio
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from bot.services.weather import get_temperature, get_weather


class TestGetTemperature(unittest.TestCase):
    def test_get_temperature(self):
        json_data = {
            "wind": 20,
            "humidity": 50,
            "other_data": {
                "main": {
                    "temporotura": 0,
                    "weather": {"pressure": 100, "temperature": 25},
                }
            },
        }
        expected_result = 25
        result = get_temperature(json_data)
        self.assertEqual(result, expected_result)


@pytest_asyncio.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_get_weather():
    message = AsyncMock()
    message.answer = AsyncMock()
    city = "Podgorica"
    await get_weather(message, city)
    message.answer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
