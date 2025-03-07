from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt # import correct
import datetime

# Initialisation de l'application
app = FastAPI(title="TouDou API", description="Une API de gestion de tâches")

# Base de données SQLite
DATABASE_URL = "sqlite:///./toudou.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle SQLAlchemy
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

#stockage utilisateurs
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# modification des taches
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# modification des utilisateurs
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


# Schémas Pydantic
class TaskCreate(BaseModel):
    title: str
    description: str

class TaskResponse(TaskCreate):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str

# Fonction de dépendance pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint : Authentification (JWT)
SECRET_KEY = "mysecretkey"

def create_token(username: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({"sub": username, "exp": expiration}, SECRET_KEY, algorithm="HS256")

@app.post("/authenticate", response_model=TokenResponse)
def authenticate(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": create_token(user.username)}

# Endpoint : Gestion des utilisateurs
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User '{username}' deleted"}


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérifier si le username est déjà utilisé par un autre utilisateur
    if user_update.username and user_update.username != db_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

    # Appliquer les modifications uniquement si elles sont fournies
    if user_update.username:
        db_user.username = user_update.username
    if user_update.password:
        db_user.password = user_update.password

    db.commit()
    db.refresh(db_user)
    
    return {"message": "User updated successfully", "user": db_user}

# Endpoint : Gestion des tâches (CRUD)
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Modifier le titre si fourni
    if task_update.title:
        db_task.title = task_update.title

    # Modifier la description si fournie
    if task_update.description:
        db_task.description = task_update.description

    db.commit()
    db.refresh(db_task)

    return {"message": f"Task {task_id} updated successfully", "task": db_task}


# Documentation Swagger accessible sur /docs

