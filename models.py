from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    builds = relationship("Build", back_populates="owner")

class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    processors = Column(String, nullable=False)
    gpus = Column(String, nullable=False)
    ram = Column(String, nullable=False)
    motherboards = Column(String, nullable=False)
    storage = Column(String, nullable=False)
    psu = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="builds")

class PCPart(Base):
    __tablename__ = "pc_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    category = Column(String, index=True)  # CPU, GPU, RAM, etc.
    current_price = Column(Float, nullable=False)
    retailer = Column(String, nullable=False)  # Amazon, Newegg, etc.
    url = Column(String, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("pc_parts.id"), nullable=False)
    price = Column(Float, nullable=False)
    date_checked = Column(DateTime, server_default=func.now())
