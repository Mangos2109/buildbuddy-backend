from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Component

router = APIRouter(
    prefix="/cpus",
    tags=["CPUs"]
)

@router.get("/")
def get_cpus(db: Session = Depends(get_db)):
    cpus = db.query(Component).filter(Component.category == "CPU").all()
    return cpus
