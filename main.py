from fastapi import FastAPI, Depends, HTTPException, Request, Response, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from enum import Enum

from base import Base, engine, SessionLocal
from models.user import User
from models.skills import Skill

# ---------------- DATABASE ----------------
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- ENUMS ----------------
class SkillCategory(str, Enum):
    programming = "programming"
    music = "music"
    sports = "sports"
    languages = "languages"
    art = "art"
    science = "science"
    cooking = "cooking"
    other = "other"

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

# ---------------- SCHEMAS ----------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SkillCreate(BaseModel):
    title: str
    description: str
    category: SkillCategory
    level: SkillLevel
    can_teach: bool
    want_learn: bool

class SkillResponse(BaseModel):
    id: int
    title: str
    description: str
    category: SkillCategory
    level: SkillLevel
    can_teach: bool
    want_learn: bool
    user_id: int

    class Config:
        from_attributes = True

# ---------------- APP ----------------
app = FastAPI(title="SkillSwap API")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- HTML ----------------
@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

# ---------------- AUTH ----------------
@app.post("/register")
def register(data: UserCreate = Body(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Користувач існує")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=data.password  # ⚠️ поки без хешу
    )
    db.add(user)
    db.commit()

    return {"message": "Реєстрація успішна ✅"}

@app.post("/login")
def login(response: Response, data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == data.username,
        User.hashed_password == data.password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Невірні дані")

    response.set_cookie(
        key="user_id",
        value=str(user.id),
        httponly=True,
        samesite="lax"
    )

    return {"message": "Вхід виконано ✅"}

@app.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не ввійшли")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Користувач не знайдений")

    return {
        "id": user.id,
        "username": user.username
    }

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie("user_id")
    return {"message": "Вихід виконано"}

# ---------------- SKILLS ----------------
@app.post("/skills", response_model=SkillResponse)
def create_skill(skill: SkillCreate, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не ввійшли")

    db_skill = Skill(
        title=skill.title,
        description=skill.description,
        category=skill.category.value,
        level=skill.level.value,
        can_teach=skill.can_teach,
        want_learn=skill.want_learn,
        user_id=int(user_id)
    )

    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill

@app.get("/skills", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не ввійшли")

    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == int(user_id)
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Навичку не знайдено або вона не ваша"
        )

    db.delete(skill)
    db.commit()

    return {"status": "deleted"}

# ---------------- RUN ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
