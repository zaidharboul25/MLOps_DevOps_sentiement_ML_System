from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import get_database_path, initialize_database
from app.routers import health, pages, texts


def create_app(database: str | Path | None = None) -> FastAPI:
    db_path = Path(database) if database is not None else get_database_path()

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        initialize_database(db_path)
        yield

    application = FastAPI(
        title="SentimentAI API", description="API V1 pour enregistrer et consulter des textes, sans classification automatique.",
        version="1.0.0", lifespan=lifespan,
    )
    application.state.database_path = db_path
    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    application.include_router(health.router)
    application.include_router(texts.router)
    application.include_router(pages.router)
    return application


app = create_app()
