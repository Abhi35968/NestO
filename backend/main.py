"""
NestO — FastAPI Main Application
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import engine, Base
import models
from routers import (auth_router, resident_router, maintenance_router,
                     visitor_router, complaint_router, notice_router, stats_router)

# ── Create DB tables ──────────────────────────────────────────
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NestO API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──────────────────────────────────────────
for router in [auth_router, resident_router, maintenance_router,
               visitor_router, complaint_router, notice_router, stats_router]:
    app.include_router(router)

# ── Serve frontend ────────────────────────────────────────────
FRONTEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND, "static")), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(os.path.join(FRONTEND, "index.html"))

@app.get("/{page}.html", include_in_schema=False)
def pages(page: str):
    fp = os.path.join(FRONTEND, f"{page}.html")
    if os.path.exists(fp):
        return FileResponse(fp)
    return FileResponse(os.path.join(FRONTEND, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

