from pydantic import BaseModel
from typing import Optional
class DoorOpenRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    name: str
    rfid_id: str
    role: str = "user"
    inside: bool = False
    department: Optional[str] = None
    mail: Optional[str] = None




