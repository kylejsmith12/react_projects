from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional
from contextlib import asynccontextmanager

# Database URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/people_db"

# SQLModel for Person
class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    occupation: str

# Pydantic models for API
class PersonCreate(SQLModel):
    first_name: str
    last_name: str
    occupation: str

class PersonUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def read_root():
    return {"message": "People Management API"}

@app.get("/people", response_model=list[Person])
def get_people():
    with Session(engine) as session:
        people = session.exec(select(Person)).all()
        return people

@app.get("/people/{person_id}", response_model=Person)
def get_person(person_id: int):
    with Session(engine) as session:
        person = session.get(Person, person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        return person

@app.post("/people", response_model=Person)
def create_person(person: PersonCreate):
    with Session(engine) as session:
        db_person = Person(**person.model_dump())
        session.add(db_person)
        session.commit()
        session.refresh(db_person)
        return db_person

@app.put("/people/{person_id}", response_model=Person)
def update_person(person_id: int, person: PersonUpdate):
    with Session(engine) as session:
        db_person = session.get(Person, person_id)
        if not db_person:
            raise HTTPException(status_code=404, detail="Person not found")
        
        person_data = person.model_dump(exclude_unset=True)
        for key, value in person_data.items():
            setattr(db_person, key, value)
        
        session.add(db_person)
        session.commit()
        session.refresh(db_person)
        return db_person

@app.delete("/people/{person_id}")
def delete_person(person_id: int):
    with Session(engine) as session:
        person = session.get(Person, person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        
        session.delete(person)
        session.commit()
        return {"message": "Person deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)