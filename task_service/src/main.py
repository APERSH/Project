from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.tasks import router as tasks_router
from api.comments import router as comments_router

app = FastAPI()

app.include_router(tasks_router)
app.include_router(comments_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port = 8002, reload = True)