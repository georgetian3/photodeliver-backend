import os
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


DATABASE_HOST: str | None = get_env("DATABASE_HOST", None)
DATABASE_PORT: int | None = int_or_none(get_env("DATABASE_PORT", None))
DATABASE_NAME: str | None = get_env("DATABASE_NAME", None)
DATABASE_USERNAME: str | None = get_env("DATABASE_USERNAME", None)
DATABASE_PASSWORD: str | None = get_env("DATABASE_PASSWORD", None)
DATABASE_DRIVERNAME: str | None = get_env("DATABASE_DRIVERNAME", None)


SERVER_PORT: int = int(get_env("SERVER_PORT", 8000))
SERVER_WORKERS: int = int(get_env("SERVER_WORKERS", 1))

ADMIN_EMAIL: str = get_env("ADMIN_EMAIL")
ADMIN_PASSWORD: str = get_env("ADMIN_PASSWORD")
