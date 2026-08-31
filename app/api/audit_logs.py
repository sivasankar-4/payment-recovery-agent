from fastapi import APIRouter

from app.database import get_audit_logs

router = APIRouter()


@router.get("/api/audit-logs")
def audit_logs():
    rows = get_audit_logs()

    return [
        {
            "event_id": row[0],
            "payment_id": row[1],
            "intent": row[2],
            "confidence": row[3],
            "recovery_score": row[4],
            "systemic": bool(row[5]),
            "retry_count": row[6],
            "action": row[7],
            "reason": row[8],
            "created_at": row[9],
        }
        for row in rows
    ]