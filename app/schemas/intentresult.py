from pydantic import BaseModel, Field

from app.schemas.intent import Intent


class IntentResult(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0.0, le=1.0)

    
