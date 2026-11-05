from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import engine
from app.routers import health


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Code after `yield` runs when the server shuts down."""
    yield
    await engine.dispose()


app = FastAPI(title="StudyNest API", lifespan=lifespan)

# Like app.use("/api", healthRouter) in Express. Next.js forwards /api/* here,
# so the browser only ever talks to one origin.
app.include_router(health.router, prefix="/api")
