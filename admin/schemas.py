from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    chat_id: int
    is_blocked: bool
    first_seen_at: datetime
    total_tokens: int | None

class MessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    text: str
    response: str
    provider_used: str
    tokens_used: int | None
    created_at: datetime