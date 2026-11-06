# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

University students in content-heavy courses, and people learning a subject on their own, who write their own notes and want help learning them. They work mainly on a laptop or desktop, in long study sessions. Phones only need to work, not shine.

The project is being built as a portfolio piece first. Use by real students comes second, but the product is designed as if real students use it.

## Product Purpose

StudyNest helps a student learn from notes they wrote themselves. Writing is treated as part of learning, so the app never writes notes for the student. It coaches them on what they wrote: answering questions from the notes, quizzing them, checking their explanations and scheduling review. It succeeds when the student understands and remembers their own material better, and every number in the app shows what they actually did.

## Positioning

Most AI study tools write the notes for the student. StudyNest does the opposite: the student writes, and the app only coaches. Every AI output is grounded only in the student's own notes, cites the paragraph it came from, and says plainly when the notes don't contain the answer.

## Operating Context

- Notes go in courses, and courses go in groups the user defines (for example, by semester).
- A course can be shared with classmates, who can read and edit it at the same time.
- Lecture slides and PDFs are uploaded alongside a course's notes.
- Study activities: writing notes (headings, lists, math), semantic search, Q&A with citations, summaries, quizzes, explain-it-back, daily review with spaced repetition, an exam planner, and stats and streaks.

## Capabilities and Constraints

- Every AI output (answers, summaries, quizzes, feedback) comes only from the user's notes and links back to its source paragraph.
- "This isn't in your notes" is a valid, first-class answer. The app never fills gaps from general knowledge.
- Stats count real attempts (quiz answers, explanation attempts, study days), never the app's estimate of what the user knows.
- A missed quiz question gets an explanation and a link to the part of the notes to reread.
- Saving a note in a shared course can conflict with another person's edit. The user must be told about the conflict, and their change must never be silently overwritten.
- Stack: Next.js (App Router) with Tailwind on the frontend, FastAPI and Postgres with pgvector on the backend. See AGENTS.md.
- Undecided: auth provider, file storage for uploads, and OpenAI model names.

## Brand Commitments

- Name: StudyNest.
- Voice: a calm coach, not hype. Feedback reads like a patient tutor. No gamified cheerleading, and streaks and stats never guilt the user.

## Evidence on Hand

None yet: no users, testimonials, usage data or press. Don't invent any.

## Product Principles

1. The student writes and the app coaches. Never take over the work that makes the learning happen.
2. Show where every claim came from. An answer without a citation to the user's notes is not an answer.
3. Honesty over helpfulness. Saying "not in your notes" beats a plausible guess.
4. Numbers are records, not judgments. Show what the user did, never what the app thinks they know.
5. Built for long, focused sessions. Calm, readable and free of distraction.

## Accessibility & Inclusion

- WCAG 2.2 AA is a hard requirement: contrast, full keyboard use, and screen reader support.
- Respect `prefers-reduced-motion`.
- Keep text dyslexia-friendly and easy to read over long sessions: comfortable line length and spacing, and no justified text.
