import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

logger = logging.getLogger(__name__)

# Like express.Router(): a group of routes that main.py mounts on the app.
router = APIRouter()


class HealthResponse(BaseModel):
    """A Pydantic model is like a zod schema. FastAPI uses it to shape the JSON
    response and to describe the route in the generated docs at /docs."""

    status: str
    database: bool


# `async def` routes share one event loop, as in Node, so database calls must be
# awaited. Depends() is how a route receives what it needs, like middleware that
# adds to `req`, except that the parameter is typed.
@router.get("/health")
async def health(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> HealthResponse:
    database = True
    try:
        # text() marks a string as raw SQL. `select 1` needs no table, so it only
        # tests that the database answers.
        await session.execute(text("select 1"))
    except Exception:
        logger.exception("Health check database query failed")
        database = False

    return HealthResponse(status="ok", database=database)
