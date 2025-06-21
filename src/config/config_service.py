from typing import get_type_hints, Union

from dotenv import load_dotenv


class AppConfigError(Exception):
    pass


class AppConfig:
    BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    CITIES: dict = {
        "Madrid": (40.416775, -3.703790),
        "Barcelona": (41.390205, 2.154007),
        "Bilbao": (43.262985, -2.935013),
    }
    HTTP_HOST: str = "weaviate"
    HTTP_PORT: int = 8080
    GRPC_PORT: int = 50051
    COLLECTION_NAME: str = "weather"
    MAX_NEW_TOKENS: int = 60
    TEMPERATURE: float = 0.15
    AZURE_OPENAI_LLM_DEPLOYMENT: str = "gpt-35-turbo"
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_EMBEDDING_ENDPOINT: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-ada-002"
    TOP_P: float = 0.9

    def __init__(self, env):
        load_dotenv()

        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError("The {} field is required".format(field))

            var_type = get_type_hints(AppConfig)[field]
            try:
                if var_type == bool:
                    value = self._parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                err_msg = (
                    'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                        env[field], var_type, field
                    )
                )

                raise AppConfigError(err_msg)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _parse_bool(val: Union[str, bool]) -> bool:
        return val if type(val) == bool else val.lower() in ["true", "yes", "1"]
