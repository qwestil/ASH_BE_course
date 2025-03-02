import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

import uvicorn
from fastapi import FastAPI, Query,  Body, Path
from src.api.hotels import router as hotels_router
from src.config import settings
from src.database import *

print(f"DB_NAME: {settings.DB_URL=}")

app = FastAPI()

app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)