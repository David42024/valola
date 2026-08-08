# fastapi/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    persona: Optional[str] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    persona: Optional[str] = None
    is_active: Optional[bool] = None


class AgentOut(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    persona: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageIn(BaseModel):
    whatsapp_number: str
    content: str = Field(..., min_length=1, max_length=2000)


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationOut(BaseModel):
    id: int
    agent_id: int
    whatsapp_number: str
    started_at: datetime
    ended_at: Optional[datetime]
    messages: List[MessageOut] = []

    model_config = {"from_attributes": True}


class TestResponse(BaseModel):
    status: str
    received: dict
    processed: bool