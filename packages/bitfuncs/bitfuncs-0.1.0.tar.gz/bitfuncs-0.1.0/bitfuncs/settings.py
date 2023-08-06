from functools import cached_property

from dynaconf import LazySettings


class Settings:
    def __init__(self):
        self._settings = LazySettings(
            ENVVAR_FOR_DYNACONF="BITFUNCS_SETTINGS",
            ENVVAR_PREFIX_FOR_DYNACONF="BITFUNCS",
        )

    @cached_property
    def bittrex_api_key(self):
        return self._settings.get("BITTREX_API_KEY")

    @cached_property
    def bittrex_api_secret(self):
        return self._settings.get("BITTREX_API_SECRET")

    @cached_property
    def degiro_int_account(self):
        return self._settings.get("DEGIRO_INT_ACCOUNT")

    @cached_property
    def degiro_password(self):
        return self._settings.get("DEGIRO_PASSWORD")

    @cached_property
    def degiro_username(self):
        return self._settings.get("DEGIRO_USERNAME")

    @cached_property
    def redis_host(self):
        return self._settings.get("REDIS_HOST", default="127.0.0.1")

    @cached_property
    def redis_port(self):
        return self._settings.get("REDIS_PORT", default=6379)


settings = Settings()
