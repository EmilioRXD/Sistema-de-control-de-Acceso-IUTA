from fastapi import APIRouter, HTTPException, Depends

from config import obtener_db
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]



@router.post("/agregar", response_model=Usuario)
async def agregar_usuario(request: Usuario, db: SessionDep) -> Usuario: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[Usuario])
async def obtener_usuarios(db: SessionDep) -> List[Usuario]:
    return crud.obtener_todos(Usuario, db)


@router.get("/{usuario_id}", response_model=Usuario)
async def obtener_usuario_por_id(usuario_id: int, db: SessionDep):
    #return db.exec(select(Usuario).filter(Usuario.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Usuario, "id", usuario_id, db=db)
    
@router.delete("/remover/{usuario_id}", response_model=Usuario)
async def remover_usuario(usuario_id: int, db: SessionDep):
    return crud.remover(Usuario, "id", usuario_id, db)


@router.patch("/actualizar/{usuario_id}", response_model=Usuario)
async def actualizar_usuario(usuario_id: int, db: SessionDep, nuevo_usuario: Usuario):
    return crud.actualizar(Usuario, usuario_id, nuevo_usuario, db)

