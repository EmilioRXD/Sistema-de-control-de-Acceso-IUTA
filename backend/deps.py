from typing import Any, Union
from datetime import datetime
from fastapi import Depends, HTTPException, status, Header
from config import obtener_db
from decouple import config
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from rutas import crud

from jose import jwt
from pydantic import ValidationError
from modelos import *

oauth = OAuth2PasswordBearer(
    tokenUrl="usuarios/login",
    scheme_name="JWT"
)

#API-KEY del dispositivo lector
async def verify_api_key(api_key: str = Header(...)):
    if api_key != config("esp32_api_key"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key


async def get_current_user(token: str = Depends(oauth), db: Session = Depends(obtener_db)) -> Usuario:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pudo validar credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario: Union[dict[str, Any], None] = crud.obtener_por_campo(Usuario,
                                                                  "correo_electronico",
                                                                  token_data.sub, db)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return usuario