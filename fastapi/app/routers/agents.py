# fastapi/app/routers/agents.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Agent, Conversation, Message
from app.schemas import AgentCreate, AgentOut, AgentUpdate
from app.services.agents import run_agent

router = APIRouter()


@router.get("/", response_model=List[AgentOut])
def list_agents(user_id: int, db: Session = Depends(get_db)):
    return db.query(Agent).filter(Agent.user_id == user_id).all()


@router.post("/inventory")
async def inventory_agent(payload: dict):
    response = run_agent(
        persona="Eres un experto en inventario de productos.",
        query=payload.get("query") or payload.get("message") or str(payload),
    )
    return {"agent": "inventory", "status": "success", "response": response}


@router.post("/finance")
async def finance_agent(payload: dict):
    response = run_agent(
        persona="Eres un analista financiero experto en pequeñas empresas.",
        query=payload.get("query") or payload.get("message") or str(payload),
    )
    return {"agent": "finance", "status": "success", "response": response}


@router.post("/", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(agent: AgentCreate, user_id: int, db: Session = Depends(get_db)):
    db_agent = Agent(user_id=user_id, **agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agent


@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: int, payload: AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    conversations = db.query(Conversation).filter(Conversation.agent_id == agent_id).all()
    for conv in conversations:
        db.query(Message).filter(Message.conversation_id == conv.id).delete()
        db.delete(conv)

    db.delete(agent)
    db.commit()
    return None