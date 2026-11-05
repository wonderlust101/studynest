# StudyNest

A study app where students write notes organized into courses, ask AI questions about them, generate quizzes, and review with spaced repetition.

This repository currently holds only the project foundation.

## Architecture

- **Frontend**: Next.js, at the repo root.
- **Backend**: FastAPI in `backend/`. It owns the API and all database access, using SQLAlchemy and Alembic.

The browser only talks to Next.js, which forwards `/api/*` to FastAPI (see `rewrites` in `next.config.ts`).

## Requirements

- [Bun](https://bun.sh)
- Node.js 22.12 or newer
- [uv](https://docs.astral.sh/uv/), which installs Python 3.14 if you don't have it
- Docker

## Getting started

```bash
bun install
cp .env.example .env.local
docker compose up -d
bun run db:migrate
```

Then run each server in its own terminal:

```bash
bun run dev:api
bun run dev
```

Open <http://localhost:3000>. <http://localhost:3000/api/health> should return `{"status":"ok","database":true}`. FastAPI's generated API docs are at <http://localhost:8000/docs>.

## Scripts

Use `bun run <script>` for all of these. `bun build` and `bun test` are Bun's own bundler and test runner, not the scripts below.

| Script        | Purpose                                                                          |
| ------------- | -------------------------------------------------------------------------------- |
| `dev`         | Start the Next.js development server                                             |
| `dev:api`     | Start the FastAPI development server                                             |
| `build`       | Create a production build of the frontend (needs `API_URL`)                      |
| `lint`        | Check frontend linting and formatting with Biome                                 |
| `format`      | Fix frontend formatting with Biome                                               |
| `typecheck`   | Generate route types and run `tsc`                                               |
| `test`        | Run frontend unit tests with Vitest                                              |
| `test:e2e`    | Run browser tests with Playwright (first run `bunx playwright install chromium`) |
| `db:generate` | Create a migration from model changes: `bun run db:generate -m "add notes"`      |
| `db:migrate`  | Apply pending migrations                                                         |

Backend checks run from the `backend/` folder:

```bash
uv run ruff check        # lint
uv run ruff format       # format
uv run mypy app tests    # type check
uv run pytest            # tests
```

## Local database

`docker-compose.yml` runs Postgres 18 with pgvector.

## Neon

`neon deploy` pulls `DATABASE_URL` (pooled, used by the app) and `DATABASE_URL_UNPOOLED` (direct, used by Alembic) into `.env.local`. While those are set, the API and `bun run db:migrate` run against the Neon branch in `.neon`, not local Docker. To use Docker, set `DATABASE_URL` to `postgres://postgres:postgres@db.localtest.me:5432/main` and remove `DATABASE_URL_UNPOOLED`.

## Deployment

`backend/Dockerfile` builds the API as a long-running container. Set `DATABASE_URL` and `DATABASE_URL_UNPOOLED` on the host, and run `.venv/bin/alembic upgrade head` as a release step. The frontend needs `API_URL` set to the API's address when it is built.
