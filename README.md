# StudyNest

A study app where students write notes organized into courses, ask AI questions about them, generate quizzes, and review with spaced repetition.

This repository currently holds only the project foundation.

## Requirements

- [Bun](https://bun.sh)
- Node.js 22.12 or newer
- Docker

## Getting started

```bash
bun install
cp .env.example .env.local
docker compose up -d
bun run db:migrate
bun run dev
```

Open <http://localhost:3000>. <http://localhost:3000/api/health> should return `{"status":"ok","database":true}`.

## Scripts

Use `bun run <script>` for all of these. `bun build` and `bun test` are Bun's own bundler and test runner, not the scripts below.

| Script        | Purpose                                                                          |
| ------------- | -------------------------------------------------------------------------------- |
| `dev`         | Start the development server                                                     |
| `build`       | Create a production build (needs `DATABASE_URL`)                                 |
| `lint`        | Check linting and formatting with Biome                                          |
| `format`      | Fix formatting with Biome                                                        |
| `typecheck`   | Generate route types and run `tsc`                                               |
| `test`        | Run unit tests with Vitest                                                       |
| `test:e2e`    | Run browser tests with Playwright (first run `bunx playwright install chromium`) |
| `db:generate` | Create a migration from schema changes                                           |
| `db:migrate`  | Apply pending migrations                                                         |
| `db:studio`   | Open Drizzle Studio to browse the database                                       |

## Local database

`docker-compose.yml` runs two services:

- **postgres**: Postgres 18 with pgvector.
- **neon-proxy**: lets the Neon driver, which sends queries over HTTP, talk to local Postgres, so the app uses the same driver locally and in production.

## Neon

`neon deploy` pulls `DATABASE_URL` (pooled, used by the app) and `DATABASE_URL_UNPOOLED` (direct, used by drizzle-kit) into `.env.local`. While those are set, the app and `bun run db:migrate` run against the Neon branch in `.neon`, not local Docker. To use Docker, set `DATABASE_URL` to `postgres://postgres:postgres@db.localtest.me:5432/main` and remove `DATABASE_URL_UNPOOLED`.
