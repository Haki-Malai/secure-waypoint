import logging

import uvicorn

from core.config import config
from core.server import app

__all__ = ["app"]


def run_application() -> None:
    """Run the FastAPI application.

    :return: None
    """
    logging.basicConfig(level=logging.INFO)
    try:
        uvicorn.run(
            app="core.server:app",
            host="0.0.0.0",
            port=8000,
            reload=config.ENVIRONMENT != "production",
            workers=1,
            log_level="info",
        )
    except Exception:
        logging.error("Failed to start Uvicorn server:", exc_info=True)


if __name__ == "__main__":
    run_application()
