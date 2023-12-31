from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas  # 모델과 스키마 정의를 임포트합니다
from .database import engine, SessionLocal
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 동일한 이메일을 가진 사용자가 있는지 확인합니다
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 비밀번호를 해시합니다
    hashed_password = pwd_context.hash(user.password)
    
    # 새 사용자 객체를 생성합니다
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    
    # 데이터베이스에 사용자를 추가하고 커밋합니다
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user