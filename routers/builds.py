from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from database import get_db
from models import Build
from schemas import BuildCreate, BuildResponse, BuildsList
from routers.auth import get_current_user  # ✅ Corrected import

router = APIRouter(prefix="/builds", tags=["Builds"])

# ✅ Save a new PC build
@router.post("/save", response_model=BuildResponse)
def save_build(build: BuildCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        new_build = Build(**build.dict(), user_id=current_user.id)
        db.add(new_build)
        db.commit()
        db.refresh(new_build)
        return new_build
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving build: {str(e)}")

# ✅ Get saved builds for the logged-in user
@router.get("/saved", response_model=BuildsList)
def get_saved_builds(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    builds = db.query(Build).filter(Build.user_id == current_user.id).all()
    return BuildsList(builds=builds)

# ✅ Update an existing PC build (NEW)
@router.put("/update/{build_id}", response_model=BuildResponse)
def update_build(
    build_id: int, updated_data: BuildCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    # Fetch the build belonging to the user
    build = db.query(Build).filter(Build.id == build_id, Build.user_id == current_user.id).first()

    if not build:
        raise HTTPException(status_code=404, detail="Build not found")

    try:
        # Update fields with new data
        for key, value in updated_data.dict().items():
            setattr(build, key, value)

        db.commit()
        db.refresh(build)
        return build
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating build: {str(e)}")

# ✅ Delete a PC build
@router.delete("/delete/{build_id}")
def delete_build(build_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Fetch the build belonging to the user
    build = db.query(Build).filter(Build.id == build_id, Build.user_id == current_user.id).first()
    
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    try:
        db.delete(build)
        db.commit()
        return {"message": "Build deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting build: {str(e)}")
