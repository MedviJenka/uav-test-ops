from functools import cache
from typing import Literal
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


LogLevel = Literal['trace', 'debug', 'info', 'notice', 'warn', 'error', 'fatal']


class __Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')

    LOGFIRE_TOKEN:        SecretStr = Field(default=SecretStr(''))
    LOGFIRE_SERVICE_NAME: str       = Field(default='uav')
    LOGFIRE_ENVIRONMENT:  str       = Field(default='dev')
    LOG_LEVEL:            LogLevel  = Field(default='info')
    OPENAI_API_KEY:       SecretStr = Field(...)
    OPENAI_MODEL:         str       = Field(default='gpt-5.5')


@cache
def __config() -> __Config:
    return __Config()


Config = __config()
