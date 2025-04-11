from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.evaluations import router as evaluation_router

app = FastAPI()

app.include_router(evaluation_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port = 8003, reload=True)