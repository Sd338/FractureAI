from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse  # Import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database setup
DATABASE_URL = "sqlite:///C:\\Users\\sd876\\OneDrive\\Desktop\\FractureAI\\fractures.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# Fracture model
class Fracture(Base):
    __tablename__ = "fractures"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Pydantic model for request validation
class FractureCreate(BaseModel):
    description: str

@app.post("/fractures/", response_model=FractureCreate)
def create_fracture(fracture: FractureCreate):
    db: Session = SessionLocal()
    new_fracture = Fracture(description=fracture.description)
    db.add(new_fracture)
    db.commit()
    db.refresh(new_fracture)
    db.close()
    return new_fracture

@app.get("/fractures/", response_model=list[FractureCreate])
def read_fractures():
    db: Session = SessionLocal()
    fractures = db.query(Fracture).all()
    db.close()
    return fractures

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the FractureAI API!"}

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "favicon.ico"))

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
