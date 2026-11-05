"""Enable the pgvector extension

Revision ID: 0001
Revises:
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # An extension adds features to Postgres. pgvector adds a `vector` column type
    # for storing embeddings. IF NOT EXISTS makes this safe to run more than once,
    # including on a database that already ran the old Drizzle migration.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
