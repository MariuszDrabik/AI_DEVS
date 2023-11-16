import logging
from typing import Dict
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from conf_dirs import ROOT_DIR
from config.log_conf import set_logger
from config.config import settings
from db.database import POSTGRES_URL

set_logger()

log = logging.getLogger("__name__")

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=f"{ROOT_DIR}/static"),
    name="static",
)
router = APIRouter()


@app.get("/")
async def health_checker(test: str = "", test_2: str = "") -> Dict[str, str]:
    print(POSTGRES_URL)
    print(settings.POSTGRES_HOST)
    return {"message": f"Hello from FastAPI for AI DEVS {test_2 or ''} {test}"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        proxy_headers=True,
    )
