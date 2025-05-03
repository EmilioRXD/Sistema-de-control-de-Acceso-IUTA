from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
from deps import verify_api_key, get_current_user

router = APIRouter()

KeyDep     = Depends(verify_api_key)
UserDep    = Depends(get_current_user)
SessionDep = Annotated[Session, Depends(obtener_db)]


#este metodo idealmente solo debe ser ejecutado por el dispositivo lector
@router.post("/agregar", dependencies=[KeyDep], response_model=RegistroAcceso)
async def agregar_registro(request: RegistroAcceso, db: SessionDep) -> RegistroAcceso: 
    return crud.añadir(request, db)
    
    
@router.get("/", dependencies=[UserDep],response_model=List[RegistroAcceso])
async def obtener_registros(db: SessionDep) -> List[RegistroAcceso]:
    return crud.obtener_todos(RegistroAcceso, db)


@router.get("/{registro_id}", dependencies=[UserDep],response_model=RegistroAcceso)
async def obtener_registro_por_id(registro_id: int, db: SessionDep):
    #return db.exec(select(RegistroAcceso).filter(RegistroAcceso.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(RegistroAcceso, "id", registro_id, db=db)
    
""""
@router.delete("/remover/{registro_id}", response_model=RegistroAcceso)
async def remover_registro(registro_id: int, db: SessionDep):
    return crud.remover(RegistroAcceso, "id", registro_id, db)


@router.patch("/actualizar/{registro_id}", response_model=RegistroAcceso)
async def actualizar_registro(registro_id: int, db: SessionDep, nuevo_registro: RegistroAcceso):
    return crud.actualizar(RegistroAcceso, registro_id, nuevo_registro, db)
"""