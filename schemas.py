
from pydantic import BaseModel
from typing import Optional, List

# Mevcut şemalar (örnek olarak)
class DoorOpenRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str
    
    surname:str
    rfid_id: str
    role: str = "user"
    inside: bool = False
    department: Optional[str] = None
    mail: Optional[str] = None

class DeleteUserRequest(BaseModel):
    username: str


class RFIDRequest(BaseModel):
    rfid_id: str

class User(BaseModel):
    id: Optional[str] = None
    name: str
    surname:str
    rfid_id: str
    role: Optional[str] = None
    inside: Optional[bool] = False
    department: Optional[str] = None
    mail: Optional[str] = None

class UserListResponse(BaseModel):
    success: bool
    message: str
    total_count: int
    users: List[User]