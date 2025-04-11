from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.meetings import router as meetings_router


app = FastAPI()

app.include_router(meetings_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port = 8004, reload=True) 