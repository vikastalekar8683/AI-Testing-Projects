from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Application as AppModel
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Job Application Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ApplicationCreate(BaseModel):
    job_title: str
    company_name: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_model: Optional[str] = None
    priority: Optional[str] = "Medium"
    status: Optional[str] = "To Apply"
    notes: Optional[str] = None

class Application(ApplicationCreate):
    id: int
    created_at: date

    class Config:
        from_attributes = True

@app.post("/applications/", response_model=Application)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    db_app = AppModel(**application.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.get("/applications/", response_model=List[Application])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = db.query(AppModel).offset(skip).limit(limit).all()
    return apps

@app.get("/applications/{application_id}", response_model=Application)
def read_application(application_id: int, db: Session = Depends(get_db)):
    app = db.query(AppModel).filter(AppModel.id == application_id).first()
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@app.put("/applications/{application_id}", response_model=Application)
def update_application(application_id: int, application: ApplicationCreate, db: Session = Depends(get_db)):
    db_app = db.query(AppModel).filter(AppModel.id == application_id).first()
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in application.dict(exclude_unset=True).items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_app = db.query(AppModel).filter(AppModel.id == application_id).first()
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_app)
    db.commit()
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
