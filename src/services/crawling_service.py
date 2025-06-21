from typing import Any
import httpx
from src.config.config_service import AppConfig


class CrawlingService:
    def __init__(self, config: AppConfig):
        self.config = config
        self._client = httpx.Client(
            base_url=self.config.BASE_URL,
            timeout=10,
        )

    def get_city_weather(self, city: str) -> dict[str, Any]:
        lat, lon = self.config.CITIES[city]
        resp = self._client.get(
            "",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh",
                "timezone": "auto",
            },
        )
        resp.raise_for_status()
        data = resp.json().get("current_weather", {})
        return {
            "city": city,
            "temperature_c": data.get("temperature"),
            "wind_speed_kmh": data.get("windspeed"),
        }

    def get_all_cities(self) -> list[dict[str, Any]]:
        return [self.get_city_weather(city) for city in self.config.CITIES]

    def close(self) -> None:
        return self._client.close()
