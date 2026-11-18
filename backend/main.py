from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime, os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ideaboard:local-dev-only-change-me@db:5432/ideaboard")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

class IdeaCreate(BaseModel):
    content: str

@app.get("/api/ideas")
def get_ideas():
    db = SessionLocal()
    ideas = db.query(Idea).all()
    db.close()
    return [{"id": i.id, "content": i.content, "created_at": i.created_at} for i in ideas]

@app.post("/api/ideas")
def create_idea(idea: IdeaCreate):
    db = SessionLocal()
    new_idea = Idea(content=idea.content)
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    db.close()
    return {"id": new_idea.id, "content": new_idea.content}
