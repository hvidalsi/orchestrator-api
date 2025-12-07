import logging
import os
import sys
from pathlib import Path

from core.config import settings


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Handler para stderr (visible en consola con FastMCP)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(getattr(logging, settings.log_level))

    # Formato detallado
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    # Handler para archivo (opcional, útil para debug)
    if settings.log_to_file:
        log_dir = Path(os.path.join(settings.root_path, "logs"))
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / f"{settings.server_name.lower().replace(' ', '_')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Evitar propagación para no duplicar logs
    logger.propagate = False

    return logger
