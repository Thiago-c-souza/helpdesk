from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import Session, select
from ..database import get_session
from ..models import Ticket, TicketCreate, TicketRead, TicketUpdate


rota = APIRouter(prefix="/tickets", tags=["tickets"])

@rota.post("/", response_model=TicketRead, status_code=201)
def criar_ticket(payload: TicketCreate, session: Session = Depends(get_session)):
    ticket = Ticket(**payload.model_dump())
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@rota.get("/", response_model=List[TicketRead])
def listar_tickets(
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None, description="aberto|em_andamento|pendente|resolvido|fechado"),
    prioridade: Optional[str] = Query(None, description="baixa|media|alta|critica"),
    responsavel: Optional[str] = None,
    solicitante: Optional[str] = None,
    q: Optional[str] = Query(None, description="busca no titulo/descrição"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = select(Ticket)
    if status:
        stmt = stmt.where(Ticket.status == status)
    if prioridade:
        stmt = stmt.where(Ticket.proioridade == prioridade)
    if responsavel:
        stmt = stmt.where(Ticket.responsavel == responsavel)
    if solicitante:
        stmt = stmt.where(Ticket.solicitante == solicitante)
    if q:
        like = f"%{q}%"
        stmt = stmt.where((Ticket.titulo.like(like)) | (Ticket.descricao.like(like)))
    stmt = stmt.order_by(Ticket.criado_em.desc()).limit(limit).offset(offset)
    return session.exec(stmt).all()

@rota.get("/{ticket_id}", response_model=TicketRead)
def obter_ticket(ticket_id: int, session:Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket não encontrado.")
    return ticket

@rota.patch("/{ticket_id}", response_model=TicketRead)
def atualizar_tickets(ticket_id: int, payload: TicketUpdate, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket não encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(ticket, k, v)
    ticket.atualizado_em = datetime.now(timezone.utc)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket