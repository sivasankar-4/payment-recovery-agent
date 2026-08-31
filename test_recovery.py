import sqlite3
from app.services.recovery import recover_payment
from app.database import DATABASE
from app.database import create_tables


create_tables()

result = recover_payment(
    message="I can pay next Monday.",
    systemic=False,
    retry_count=0,
    recovery_score=95,
    event_id="evt_audit_001",
    payment_id="pay_audit_001",
)

print("Final result:")
print(result)


connection = sqlite3.connect(DATABASE)

row = connection.execute("""
    SELECT
        event_id,
        payment_id,
        intent,
        confidence,
        recovery_score,
        systemic,
        retry_count,
        action,
        reason
    FROM audit_logs
    WHERE event_id = ?
""", ("evt_audit_001",)).fetchone()

connection.close()

print("\nAudit record:")
print(row)