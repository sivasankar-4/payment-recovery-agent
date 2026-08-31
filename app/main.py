from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.webhook_controller import router as webhook_router
from app.api.payments import router as payments_router
from app.api.audit_logs import router as audit_logs_router

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import create_tables


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(payments_router)
app.include_router(audit_logs_router)

app.mount(
    "/assets",
    StaticFiles(directory=FRONTEND_DIST / "assets"),
    name="assets",
)

@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_DIST / "index.html")

create_tables()


@app.get("/health")
def health_check():
    return {"status": "Recovery agent is running"}