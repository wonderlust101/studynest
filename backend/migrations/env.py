from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# Importing models registers every table on Base.metadata.
import app.models  # noqa: F401
from app.config import settings
from app.db import Base

if context.config.config_file_name:
    fileConfig(context.config.config_file_name)

# Migrations run one at a time, so a plain synchronous connection is enough.
engine = create_engine(settings.migration_database_url)

with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()
