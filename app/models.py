from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from enum import Enum

class PrioridadeEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"

class StatusEnum(str, Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    pendente = "pendente"
    resolvido = "resolvido"
    fechado = "fechado"

class TicketBase(SQLModel):
    titulo: str
    descricao: str
    solicitante: str
    proioridade: PrioridadeEnum = PrioridadeEnum.media
    status: str = StatusEnum.aberto
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
    prioridade: Optional[PrioridadeEnum] = None
    status: Optional[StatusEnum] = None
    responsavel: Optional[str] = None