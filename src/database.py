from sqlmodel import create_engine, SQLModel, Session
from src.config import settings

engine = create_engine(settings.database_url)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
