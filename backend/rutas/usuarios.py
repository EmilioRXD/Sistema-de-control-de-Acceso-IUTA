from fastapi import APIRouter, HTTPException, Depends, status, Path, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from config import obtener_db
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)
from rutas.deps import *

router = APIRouter()


@router.get("/me", response_model=Usuario)
async def obtener_usuario_actual(user: Usuario = Depends(get_current_user)):
    """Obtiene la sesión de usuario actual."""
    return user


@router.post("/agregar", dependencies=None, response_model=UsuarioForm)
async def registrar(request: UsuarioForm, db: SessionDep):
    """Registrar un nuevo usuario administrador"""
    usuario = crud.obtener_por_campo(Usuario, "correo_electronico",request.correo_electronico, db)
    if usuario is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario con este correo ya existe"
        )
    
    data = Usuario(
        nombre=request.nombre,
        apellido=request.apellido,
        correo_electronico=request.correo_electronico,
        contraseña=get_hashed_password(request.contraseña)
        )
    usuario = crud.añadir(data, db)
    return usuario
    
@router.post("/login", response_model=Token)
async def iniciar_sesion(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = crud.obtener_por_campo(Usuario, "correo_electronico", form_data.username, db)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo o contraseña incorrectos"
        )
    
    hashed_pass = usuario.contraseña
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo o contraseña incorrectos"
        )

    return {
        "access_token": create_access_token(usuario.correo_electronico),
        "refresh_token": create_refresh_token(usuario.correo_electronico)
    }


@router.get("/", dependencies=[UserDep],response_model=List[Usuario])
async def obtener_usuarios(db: SessionDep) -> List[Usuario]:
    """Obtiene una lista con todos los usuarios registrados en el sistema."""
    return crud.obtener_todos(Usuario, db)


@router.get("/{usuario_correo}", dependencies=[UserDep],response_model=Usuario)
async def obtener_usuario_por_correo(usuario_correo: str, db: SessionDep):
    """Obtiene los datos de un usuario (nombre, apellido) mediante el correo"""
    #return db.exec(select(Usuario).filter(Usuario.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Usuario, "correo_electronico", usuario_correo, db=db)

    
@router.delete("/remover/{usuario_correo}", dependencies=[UserDep],response_model=Usuario)
async def remover_usuario(usuario_correo: str, db: SessionDep):
    """Remueve del sistema el usuario correspondiente al correo específicado"""
    usuario = crud.obtener_por_campo(Usuario, "correo_electronico", usuario_correo, db)
    return crud.remover(Usuario, "id", usuario.id, db)


@router.patch("/actualizar/{usuario_correo}", dependencies=[UserDep],response_model=Usuario)
async def actualizar_usuario(usuario_correo: str, db: SessionDep, nuevo_usuario: Usuario):
    """Actualizar datos del usuario correspondiente al correo específicado"""
    usuario = crud.obtener_por_campo(Usuario, "correo_electronico", usuario_correo, db)
    return crud.actualizar(Usuario, usuario.id, nuevo_usuario, db)

