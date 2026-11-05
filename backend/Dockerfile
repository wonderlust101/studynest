FROM python:3.14-slim

# uv installs the exact versions pinned in uv.lock.
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /usr/local/bin/uv

WORKDIR /srv

# Copied before the code so that code changes don't reinstall every dependency.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev

COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app

# Don't run the server as root.
RUN useradd --create-home appuser
USER appuser

# DATABASE_URL comes from the host's environment settings. Run migrations as a
# separate release step: `.venv/bin/alembic upgrade head`.
EXPOSE 8000
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
