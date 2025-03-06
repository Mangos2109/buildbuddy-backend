from fastapi import APIRouter
from models import Component  # Import the Component model
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.get("/")
def get_components(db: Session = Depends(get_db)):
    return db.query(Component).all()
