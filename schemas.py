from pydantic import BaseModel, EmailStr
from typing import Optional

# ----------- Esquemas para Usuarios -----------

# Datos que el cliente envía al registrar un usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
# Datos que devolvemos al cliente (sin contraseña)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# ----------- Esquemas para Autenticación -----------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str