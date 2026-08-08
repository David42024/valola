# fastapi/app/routers/whatsapp.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Agent, Conversation, Message
from app.schemas import MessageIn, MessageOut

router = APIRouter()


@router.post("/webhook", response_model=MessageOut)
async def receive_message(payload: MessageIn, agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.agent_id == agent_id,
            Conversation.whatsapp_number == payload.whatsapp_number,
            Conversation.ended_at.is_(None),
        )
        .order_by(Conversation.started_at.desc())
        .first()
    )

    if not conversation:
        conversation = Conversation(agent_id=agent_id, whatsapp_number=payload.whatsapp_number)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message