from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./helpdesk.db"

engine = create_engine(DATABASE_URL, echo=False)

def criar_db_tabelas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session