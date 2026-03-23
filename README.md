# 🌱 AgroGalaxy Backend

API REST construida con **FastAPI** y **SQLite** para gestión de usuarios con autenticación JWT.

---

## Estructura del proyecto

```
Backend-Agrogalaxy/
├── README.md
├── .gitignore
├── main.py         # Punto de entrada, rutas de la API
├── models.py       # Modelos de la base de datos (SQLAlchemy)
├── schemas.py      # Esquemas de validación (Pydantic)
├── crud.py         # Operaciones de base de datos
├── database.py     # Configuración de la DB y sesión
└── security.py     # JWT, autenticación y dependencias
```

---

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/Geraldine04Umasi/Backend-Agrogalaxy.git
cd Backend-Agrogalaxy
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] pydantic[email]
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Puedes generar una clave segura con:
> ```python
> import secrets; print(secrets.token_urlsafe(32))
> ```

### 4. Correr el servidor

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

---

## Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/` | Health check | ❌ |
| POST | `/users/` | Registrar usuario | ❌ |
| GET | `/users/` | Listar usuarios | ❌ |
| GET | `/users/{id}` | Obtener usuario | ❌ |
| PUT | `/users/{id}` | Actualizar usuario | ❌ |
| DELETE | `/users/{id}` | Eliminar usuario | ❌ |
| POST | `/login` | Login (obtener JWT) | ❌ |
| GET | `/me` | Info del usuario actual | ✅ |

---

## Autenticación

La API usa **JWT (JSON Web Tokens)** con el algoritmo `HS256`.

Para acceder a rutas protegidas, incluye el token en el header:

```
Authorization: Bearer <tu_token>
```

---

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [python-jose](https://python-jose.readthedocs.io/)
- [passlib](https://passlib.readthedocs.io/)

---

## Notas

- La base de datos `agrogalaxy.db` se genera automáticamente al iniciar el servidor.
- La documentación interactiva está disponible en `http://localhost:8000/docs`.
