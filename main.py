from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers.auth import router as auth_router
from routers.builds import router as builds_router
from routers.parts import router as parts_router
from pydantic import BaseModel
from routers.price_tracking import router as price_tracking_router
from routers.cpus import router as cpus_router
from typing import List
from databases import Database
from routers.components import router as components_router  # ✅ Ensure this is correct

# ✅ Initialize FastAPI app (This must be BEFORE registering routers)
app = FastAPI(title="BuildBuddy API", description="API for BuildBuddy Custom PC Builder", version="1.0")

# ✅ Register routers AFTER initializing app
app.include_router(auth_router)
app.include_router(builds_router)
app.include_router(parts_router)
app.include_router(price_tracking_router, prefix="/prices")  # ✅ Corrected placement
app.include_router(cpus_router, prefix="/cpus")
app.include_router(parts_router, prefix="/parts")
app.include_router(components_router, prefix="/components")  # ✅ Ensure this is included

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Test endpoint to check if API is running
@app.get("/status")
def status_check():
    return {"status": "API is running"}

# ✅ Home route
@app.get("/")
def home():
    return {"message": "Welcome to BuildBuddy!"}

@app.get("/api/components")
async def get_components():
    query = "SELECT * FROM components WHERE category='CPU'"
    return await database.fetch_all(query)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
