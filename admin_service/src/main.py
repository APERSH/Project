from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.teams import router as teams_router
from api.departments import router as dep_router
from api.news import router as news_router
from api.users import router as users_router

app = FastAPI()
app.include_router(teams_router)
app.include_router(dep_router)
app.include_router(news_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port = 8001, reload=True) 