from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import criar_db_tabelas
from .routers import tickets

@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_db_tabelas()
    yield

app = FastAPI(
    title="Helpdesk CRUD",
    description=" API chamados (OS) - estutura + banco + modelos",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tickets.rota)

@app.get("/")
def root():
    return {"ok": True, "msg": "Banco e modelos conectados, proximo: CRUD de tickets."}