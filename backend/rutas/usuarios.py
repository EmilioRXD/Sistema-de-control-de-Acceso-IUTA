from fastapi import APIRouter, HTTPException, Depends, status
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
from deps import get_current_user, verify_api_key



router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]

UserDep = Depends(get_current_user)

@router.get("/me", response_model=Usuario)
async def obtener_usuario_actual(user: Usuario = Depends(get_current_user)):
    return user


@router.post("/agregar", dependencies=None, response_model=UsuarioForm)
async def registrar(request: UsuarioForm, db: SessionDep): 
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
    return crud.obtener_todos(Usuario, db)


@router.get("/{usuario_id}", dependencies=[UserDep],response_model=Usuario)
async def obtener_usuario_por_id(usuario_id: int, db: SessionDep):
    #return db.exec(select(Usuario).filter(Usuario.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Usuario, "id", usuario_id, db=db)

    
@router.delete("/remover/{usuario_id}", dependencies=[UserDep],response_model=Usuario)
async def remover_usuario(usuario_id: int, db: SessionDep):
    return crud.remover(Usuario, "id", usuario_id, db)


@router.patch("/actualizar/{usuario_id}", dependencies=[UserDep],response_model=Usuario)
async def actualizar_usuario(usuario_id: int, db: SessionDep, nuevo_usuario: Usuario):
    return crud.actualizar(Usuario, usuario_id, nuevo_usuario, db)

