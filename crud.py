from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Para encriptar y verificar contraseñas
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# CRUD Operations
# Crear nuevo usuario
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Obtener usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Obtener usuario por email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Obtener usuario por username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Obtener lista de usuarios (con límite opcional)
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# Actualizar usuario
def update_user(db: Session, user_id: int, update_data: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    if "username" in update_data and update_data["username"] is not None:
        db_user.username = update_data["username"]
    if "email" in update_data and update_data["email"] is not None:
        db_user.email = update_data["email"]
    if "password" in update_data and update_data["password"] is not None:
        db_user.hashed_password = get_password_hash(update_data["password"])

    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar usuario
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# Nota: Las funciones de actualización y eliminación retornan None si el usuario no existe.

# Autenticar usuario
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user