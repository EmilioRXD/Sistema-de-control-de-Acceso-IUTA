from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/agregar", response_model=Estudiante)
async def agregar_estudiante(request: Estudiante, db: SessionDep) -> Estudiante: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[Estudiante])
async def obtener_estudiantes(db: SessionDep) -> List[Estudiante]:
    return crud.obtener_todos(Estudiante, db)


@router.get("/{estudiante_cedula}", response_model=Estudiante)
async def obtener_estudiante_por_cedula(estudiante_cedula: str, db: SessionDep):
    #return db.exec(select(Estudiante).filter(Estudiante.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Estudiante, "cedula", estudiante_cedula, db=db)
    
@router.delete("/remover/{estudiante_cedula}", response_model=Estudiante)
async def remover_estudiante(estudiante_cedula: str, db: SessionDep):
    return crud.remover(Estudiante, "cedula", estudiante_cedula, db)


@router.patch("/actualizar/{estudiante_cedula}", response_model=Estudiante)
async def actualizar_estudiante(estudiante_cedula: str, db: SessionDep, nuevo_est: Estudiante):
    return crud.actualizar(Estudiante, estudiante_cedula, nuevo_est, db)

@router.get("/tarjeta/{estudiante_cedula}", response_model=TarjetaNFC)
async def obtener_tarjeta(estudiante_cedula: str, db: SessionDep) -> TarjetaNFC:
    query = select(TarjetaNFC).filter(TarjetaNFC.estudiante_cedula == estudiante_cedula)
    return db.exec(query).scalars().first()