
<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# StudyNest: guide for coding agents

Read this whole file before changing anything. If a rule here conflicts with a request, ask the user.

## 1. What StudyNest is

StudyNest is a study app for students who write their own notes and want help learning them. Most AI study tools write the notes for the student. StudyNest does the opposite: the student writes, because writing is part of learning, and the app coaches them on what they wrote.

It's for university students in content-heavy courses and for anyone learning a subject on their own.

**Product rules. Every feature must follow these:**

- **Grounded.** Every AI output (answers, summaries, quizzes, feedback) comes only from the user's own notes and links back to the paragraph it came from.
- **Honest.** If the notes don't contain the answer, say so. Never guess or fill gaps from general knowledge.
- **Real stats.** Every number shown counts what the user actually did, never the app's estimate of what they know.

## 2. Features

- **Editor:** headings, lists and math.
- **Organization:** notes go in courses, and courses go in user-defined groups (for example, by semester).
- **Sharing:** a course can be shared with classmates, who can read and edit it.
- **Uploads:** lecture slides and PDFs stored alongside a course's notes.
- **Semantic search:** finds notes by meaning, not just exact words.
- **Q&A:** answers questions from the user's notes, with a citation to each source paragraph.
- **Summaries:** short or detailed, for each note and each course. They update when the notes change.
- **Quizzes:** built from one note, a topic or a whole course. A missed question gets an explanation and a link to the part of the notes to reread.
- **Explain it back:** the user explains a section in their own words, and the app points out what they left out or got wrong.
- **Daily review:** spaced repetition of missed questions and explanation prompts.
- **Exam planner:** given an exam date, plans each day until then, weighted toward the notes with the most missed questions.
- **Stats and streaks:** quiz scores over time, questions answered and study days completed.

## 3. Architecture

- **Next.js (repo root)** is the frontend only. The browser calls `/api/*`, and `next.config.ts` forwards those requests to FastAPI.
- **FastAPI (`backend/`)** owns all database access and all AI calls. Don't add Next.js route handlers or Server Actions for data.
- **Database:** Postgres, with pgvector for embeddings. Access goes through SQLAlchemy (async), and schema changes go through Alembic migrations. It runs in Docker locally and on Neon in the cloud.
- **Hosting:** backend on Railway (`backend/Dockerfile`), frontend on Vercel.
- **Environment variables:** read them only through `backend/app/config.py` and `src/lib/env.ts`, never from `os.environ` or `process.env` directly.

Planned backend layout. Create each folder when the first feature needs it, not before:

| Folder                  | Holds                                                          |
| ----------------------- | -------------------------------------------------------------- |
| `backend/app/routers/`  | HTTP endpoints only. Parse the request, call a service, return. |
| `backend/app/schemas/`  | Pydantic request and response models                            |
| `backend/app/models/`   | SQLAlchemy table classes                                        |
| `backend/app/services/` | Business logic. Plain functions that are easy to test           |
| `backend/app/ai/`       | The only code that talks to OpenAI                              |

**Open decisions (TODO, ask before choosing):** auth provider, file storage for uploads, and OpenAI model names.

## 4. Workflow for every change

1. **Understand first.** Read the files you will touch, the code that calls them, and their tests. Search for every usage before you rename something or change a function signature.
2. **Write a failing test** (see section 6).
3. **Write the simplest code that makes it pass.**
4. **Check the side effects.** Does the change need a migration? Does it change an API response the frontend relies on? Does it add an env var (update `.env.example`, both config files and the README)? Does CI still pass?
5. **Run every check** in section 10.
6. **Ask before adding any dependency**, whether npm or Python.

## 5. Code style: readable before clever

The code should be easy for a person to read on the first pass.

- **Smallest change that works.** Don't add speculative options, flags, config or generic helpers. Only extract a shared abstraction once three real uses exist.
- **Clear names.** Use full words (`course_id`, not `cid`). Functions are verbs, and booleans read as questions (`is_shared`).
- **Small functions** that each do one thing. Use early returns instead of deep nesting.
- **Comments explain why**, not what. The first time a Next.js, SQL or Python concept appears in a file, add a one-line explanation. The user comes from MERN, so comparisons to Express or Mongoose help.
- **Follow the existing patterns** in the repo before inventing new ones.
- **No dead code**, commented-out code or unrelated reformatting in a change.
- **Handle errors explicitly.** Return clear HTTP errors (`404`, `403`, `422`) with a useful message. Never swallow an exception silently.

**Python**

- Type everything. mypy runs in strict mode.
- SQLAlchemy 2.0 style: `select(...)` with `await session.execute(...)`. Get the session with `Depends(get_session)`.
- Every request body and response is a Pydantic model. Never return a raw table object.

**TypeScript and React**

- No `any`. Validate data from outside the code (forms, API responses) with zod.
- Use Server Components by default. Add `"use client"` only for components that need state, effects or browser events.
- Style with Tailwind.

**Efficiency, without making code harder to read**

- Avoid N+1 queries: load related rows in one query.
- Paginate lists that can grow.
- Add a database index for columns used in filters and joins.
- Batch embedding requests.
- Don't optimize anything else without a measured reason.

## 6. Testing

**Test first for all logic.** Backend endpoints, services and pure functions (Python or TypeScript) start with a failing test. Write the test, run it and watch it fail, then write the code.

- **Bug fixes** start with a test that reproduces the bug.
- **UI components** can get tests alongside or after the code. Each critical user flow (write a note, ask a question, take a quiz) gets a Playwright test.
- Each test checks **one behavior** and has a name that describes it, for example `test_quiz_rejects_answers_from_other_users`.
- Test the edge cases: empty input, missing records, another user's data, and the "not in your notes" path.
- **Never call OpenAI in tests.** Replace the `app/ai/` functions with fakes. Follow the fake-database pattern already in `backend/tests/`.

| Kind              | Location                    | Tool       |
| ----------------- | --------------------------- | ---------- |
| Backend           | `backend/tests/test_*.py`   | pytest     |
| Frontend unit     | `src/**/*.test.ts(x)`       | Vitest     |
| End-to-end        | `tests/e2e/*.spec.ts`       | Playwright |

## 7. Security and data safety

- **Check access in the backend.** Every query must be limited to courses the current user owns or that were shared with them. Hiding a button in the UI is not access control.
- **Validate all input** with Pydantic on the backend and zod on the frontend.
- **Never build SQL from strings.** Use SQLAlchemy queries, which pass values as parameters.
- **Uploads are private.** Enforce size and file type limits, and never serve uploads from a public URL.
- **Secrets** go only in `.env.local` and the host's environment settings. Never commit or log them.
- **Prompt injection.** Note text and uploaded files are untrusted. In AI prompts, wrap them in clearly marked data sections, and never let them change the instructions.
- **Concurrent edits.** Shared courses can be edited by several people at once. Saving a note must not silently overwrite someone else's change, so check a version number or `updated_at` and return `409 Conflict` when it's out of date.

## 8. AI rules

- **One entry point.** Every OpenAI call (generation and embeddings) lives in `backend/app/ai/`. Model names come from config, never hard-coded.
- **Grounded answers.** Retrieve the relevant note chunks, tell the model to answer only from them, and return a citation (note id and paragraph id) for each claim. "This isn't in your notes" is a valid, tested answer.
- **Structured output.** Ask for JSON that matches a Pydantic model and validate it. Never parse free text with string tricks.
- **Update only what changed.** When a note changes, recompute embeddings and summaries for that note (and its course summary), not for everything.
- **Record real attempts.** Store every quiz answer and explanation attempt. Review scheduling, exam plans and stats are all computed from those records.

## 9. Database and migrations

- Every schema change gets an Alembic migration: `bun run db:generate -m "add notes"`.
- Read the generated migration before applying it, because autogenerate can miss or misread changes. Make sure `downgrade` works.
- Never edit a migration that has already been applied. Add a new one instead.
- Add foreign keys with an explicit `ondelete` rule, and add indexes for foreign keys used in filters.

## 10. Commands

Run these before calling any change finished.

```bash
# Frontend (repo root). Use `bun run test`, not `bun test`: those are different tools.
bun run lint
bun run typecheck
bun run test
bun run test:e2e   # when UI flows changed

# Backend (from backend/)
uv run ruff check
uv run ruff format
uv run mypy app tests
uv run pytest
```

## 11. Definition of done

- Tests were written first, and they pass.
- Every check in section 10 passes.
- The diff has no unrelated changes, debug code or leftover TODOs.
- `.env.example` and `README.md` are updated if setup or env vars changed.
- You've explained the change to the user in plain words, including anything you couldn't verify.
