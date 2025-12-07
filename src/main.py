from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import routes
from core.config import settings
from core.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Iniciando {settings.server_name} {settings.server_version}")
    logger.info(f"Modo de depuración: {settings.environment}")
    yield

    logger.info(f"Cerrando {settings.server_name}")


app = FastAPI(
    title=settings.server_name,
    description="Api de Canal que orquesta los servicios de STT y TTS con el Agente Bancario",
    version=settings.server_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.health)
app.include_router(routes.agent)


@app.get("/")
def root():
    """
    Endpoint raíz
    """
    return {
        "message": f"Bienvenido a {settings.server_name}",
        "docs": "/docs",
        "version": "settings.server_version",
    }
