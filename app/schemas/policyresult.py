from pydantic import BaseModel
from app.schemas.action import Action

class PolicyResult(BaseModel):
    action : Action
    reason : str