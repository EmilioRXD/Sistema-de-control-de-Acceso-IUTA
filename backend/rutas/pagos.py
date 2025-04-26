from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/agregar", response_model=Pago)
async def agregar_pago(request: Pago, db: SessionDep) -> Pago: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[Pago])
async def obtener_pagos(db: SessionDep) -> List[Pago]:
    return crud.obtener_todos(Pago, db)


@router.get("/{pago_id}", response_model=Pago)
async def obtener_pago_por_id(pago_id: int, db: SessionDep):
    #return db.exec(select(Pago).filter(Pago.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Pago, "id", pago_id, db=db)


@router.get("/{cedula_estudiante}", response_model=List[Pago])
async def obtener_pagos_de_estudiante(cedula_estudiante: str, db: SessionDep) -> List[Pago]:
    query = select(Pago).filter(Pago.estudiante_cedula == cedula_estudiante)
    return db.exec(query).scalars().all()


