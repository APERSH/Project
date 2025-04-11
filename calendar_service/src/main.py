from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.calendar import router as calendar_router

app = FastAPI()

app.include_router(calendar_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port = 8005, reload=True)