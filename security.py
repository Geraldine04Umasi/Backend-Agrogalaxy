import os
from datetime import datetime, timedelta
from typing import Optional, Generator

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
import crud

# -------------------- CONFIG --------------------
# Cambia SECRET_KEY en producción (usa .env). Puedes generar uno con:
# >>> import secrets; secrets.token_urlsafe(32)
SECRET_KEY = os.environ.get("SECRET_KEY", "cambia_esto_por_una_clave_muy_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# -------------------- Seguridad --------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT que incluye la información en `data`.
    Se recomienda pasar `{"sub": username}` en data.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_db() -> Generator[Session, None, None]:
    """Dependencia para obtener una sesión de DB (igual a la que tienes en main.py)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_username_from_token(token: str) -> str:
    """
    Decodifica el token y devuelve el username (campo 'sub').
    Lanza HTTPException 401 si no se puede validar.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependencia para rutas protegidas: devuelve el usuario autenticado (objeto SQLAlchemy).
    Uso en rutas: current_user = Depends(security.get_current_user)
    """
    username = _get_username_from_token(token)
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

