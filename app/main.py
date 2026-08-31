from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.webhook_controller import router as webhook_router
from app.api.payments import router as payments_router
from app.api.audit_logs import router as audit_logs_router

from app.database import create_tables


app = FastAPI()

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

create_tables()


@app.get("/health")
def health_check():
    return {"status": "Recovery agent is running"}