import os
from dataclasses import dataclass, field
from typing import Any, TypeVar

from dotenv import load_dotenv


class _NoDefault: ...


class MissingEnvironmentVariable(Exception): ...


T = TypeVar("T")


def get_env(variable: str, default: T | _NoDefault = _NoDefault()) -> str | T:
    try:
        return os.environ[variable]
    except KeyError:
        if isinstance(default, _NoDefault):
            raise MissingEnvironmentVariable(
                f"Missing environment variable: {variable}"
            )
        return default


def int_or_none(x: Any) -> int | None:
    try:
        return int(x)
    except Exception:
        return None


load_dotenv()


@dataclass
class DatabaseConfig:
    HOST: str | None = get_env("DATABASE_HOST", None)
    PORT: int | None = int_or_none(get_env("DATABASE_PORT", None))
    DATABASE: str | None = get_env("DATABASE_DATABASE", None)
    USERNAME: str | None = get_env("DATABASE_USERNAME", None)
    PASSWORD: str | None = get_env("DATABASE_PASSWORD", None)
    DRIVERNAME: str | None = get_env("DATABASE_DRIVERNAME", None)


@dataclass
class ServerConfig:
    PORT: int = int(get_env("SERVER_PORT", 8000))
    WORKERS: int = int(get_env("SERVER_WORKERS", 1))

@dataclass
class AuthConfig:
    ...