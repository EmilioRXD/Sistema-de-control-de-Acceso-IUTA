from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/añadir", response_model=Pago)
async def añadir_pago(request: Pago, db: SessionDep) -> Pago: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[Pago])
async def obtener_pagos(db: SessionDep) -> List[Pago]:
    return crud.obtener_todos(Pago, db)


@router.get("/{pago_id}", response_model=Pago)
async def obtener_pago_por_id(pago_id: int, db: SessionDep):
    #return db.exec(select(Pago).filter(Pago.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(Pago, "id", pago_id, db=db)


#no se si deberia estar o no 

@router.delete("/remover/{pago_id}", response_model=Pago)
async def remover_pago(pago_id: int, db: SessionDep):
    return crud.remover(Pago, "id", pago_id, db)



#@router.patch("/actualizar/{pago_id}", response_model=Pago)
#async def actualizar_pago(pago_id: int, db: SessionDep, nuevo_pago: Pago):
#    return crud.actualizar(Pago, pago_id, nuevo_pago, db)