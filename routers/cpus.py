from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Component  # Ensure your models are imported

app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/cpus/")
def get_cpus(db: Session = Depends(get_db)):
    cpus = db.query(Component).filter(Component.category == "CPU").all()
    return cpus
