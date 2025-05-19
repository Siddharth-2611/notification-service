from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: int
    type: str  # 'email', 'sms', 'in_app'
    subject: Optional[str] = None
    message: str
