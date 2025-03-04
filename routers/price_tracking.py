from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PCPart, PriceHistory
from .price_scraper import scrape_amazon_product

router = APIRouter()  # ✅ No prefix here

# ✅ Fix: Remove extra `/prices` from route paths
@router.get("/latest")  # 🔥 Change from "/prices/latest" to "/latest"
def get_latest_prices(db: Session = Depends(get_db)):
    parts = db.query(PCPart).all()
    return [{"name": p.name, "price": p.current_price, "retailer": p.retailer} for p in parts]

@router.post("/update/{part_id}")  # 🔥 Change from "/prices/update/{part_id}" to "/update/{part_id}"
def update_price(part_id: int, db: Session = Depends(get_db)):
    part = db.query(PCPart).filter(PCPart.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    new_price = scrape_amazon_product(part.url)  # Scrape price

    if new_price:
        part.current_price = new_price
        db.add(PriceHistory(part_id=part.id, price=new_price))
        db.commit()
        return {"message": "Price updated", "new_price": new_price}
    else:
        raise HTTPException(status_code=400, detail="Failed to retrieve new price")
