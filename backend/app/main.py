from fastapi import FastAPI
from . import webhook

import logging

# Force root logger to DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Create app-specific logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

logger.debug("🚀 Debug logging is enabled in main.py")


# Also explicitly adjust uvicorn loggers
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ready")
def ready():
    return {"ready": True}

app.include_router(webhook.router)
