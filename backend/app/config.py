from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# The repo root's .env.local is shared with Next.js, so both apps read one file.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env.local"


def to_sqlalchemy_url(url: str) -> str:
    """Add the driver name SQLAlchemy needs. It rejects a plain postgres:// URL."""
    _, separator, rest = url.partition("://")
    if not separator:
        raise ValueError("DATABASE_URL must look like postgres://user:pass@host/db")
    return f"postgresql+psycopg://{rest}"


class Settings(BaseSettings):
    """Like src/lib/env.ts with zod: fields are read from the environment by name
    (DATABASE_URL fills database_url), and a missing one fails at startup."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        # .env.local also holds variables meant for other tools.
        extra="ignore",
        # Treat `FOO=` as missing rather than as a valid empty string.
        env_ignore_empty=True,
    )

    database_url: str
    # Neon only. Its pooled URL can't hold the session state migrations rely on.
    database_url_unpooled: str | None = None

    @property
    def app_database_url(self) -> str:
        return to_sqlalchemy_url(self.database_url)

    @property
    def migration_database_url(self) -> str:
        return to_sqlalchemy_url(self.database_url_unpooled or self.database_url)


settings = Settings()
