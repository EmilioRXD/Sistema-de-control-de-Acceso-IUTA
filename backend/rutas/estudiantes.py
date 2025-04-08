from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/añadir", response_model=Estudiante)
async def añadir_estudiante(request: Estudiante, db: SessionDep) -> Estudiante: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[Estudiante])
async def obtener_estudiante(db: SessionDep) -> List[Estudiante]:
    return crud.obtener_todos(Estudiante, db)


@router.get("/{estudiante_id}", response_model=Estudiante)
async def obtener_estudiante_por_id(estudiante_id: int, db: SessionDep):
    #return db.exec(select(Estudiante).filter(Estudiante.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Estudiante, "id", estudiante_id, db=db)
    
@router.delete("/remover/{estudiante_id}", response_model=Estudiante)
async def remover_estudiante(estudiante_id: int, db: SessionDep):
    return crud.remover(Estudiante, "id", estudiante_id, db)


@router.patch("/actualizar/{estudiante_id}", response_model=Estudiante)
async def actualizar_estudiante(estudiante_id: int, db: SessionDep, nuevo_est: Estudiante):
    return crud.actualizar(Estudiante, estudiante_id, nuevo_est, db)