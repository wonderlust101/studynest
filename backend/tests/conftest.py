import os

# app.config fails without this. Tests never connect to it, so CI needs no database.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
