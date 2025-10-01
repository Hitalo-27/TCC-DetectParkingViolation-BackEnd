from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed_password = auth.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_email: str = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.put("/update")
def update_user(
    update: schemas.UserUpdate,  # schema que vamos criar
    current_email: str = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualiza username
    if update.username:
        user.username = update.username
    
    # Atualiza email
    if update.email:
        # verifica se o email já existe
        existing_user = db.query(models.User).filter(models.User.email == update.email).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        user.email = update.email
    
    # Atualiza senha
    if update.old_password or update.new_password or update.new_password_confirm:
        if not update.old_password or not update.new_password or not update.new_password_confirm:
            raise HTTPException(status_code=400, detail="Preencha todas as senhas para alterar")
        
        if not auth.verify_password(update.old_password, user.password):
            raise HTTPException(status_code=400, detail="Senha antiga incorreta")
        
        if update.new_password != update.new_password_confirm:
            raise HTTPException(status_code=400, detail="Novas senhas não conferem")
        
        user.password = auth.hash_password(update.new_password)
    
    db.commit()
    db.refresh(user)
    
    return {"message": "Usuário atualizado com sucesso"}
