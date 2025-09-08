from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class TicketBase(SQLModel):
    titulo: str
    descricao: str
    solicitante: str
    proioridade: str = "media"
    status: str = "aberto"
    responsavel: Optional[str] = None

class Ticket(TicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class TicketCreate(TicketBase):
    pass

class TicketRead(TicketBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

class TicketUpdate(SQLModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    solicitante: Optional[str] = None
    prioridade: Optional[str] = None
    status: Optional[str] = None
    responsavel: Optional[str] = None