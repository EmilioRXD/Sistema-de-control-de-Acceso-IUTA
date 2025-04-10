from fastapi import APIRouter, HTTPException, Path, Depends

from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/añadir", response_model=TarjetaNFC)
async def añadir_tarjeta(request: TarjetaNFC, db: SessionDep) -> TarjetaNFC: 
    return crud.añadir(request, db)
    
    
@router.get("/", response_model=List[TarjetaNFC])
async def obtener_tarjetas(db: SessionDep) -> List[TarjetaNFC]:
    return crud.obtener_todos(TarjetaNFC, db)


@router.get("/{tarjeta_id}", response_model=TarjetaNFC)
async def obtener_tarjeta_por_id(tarjeta_id: int, db: SessionDep):
    #return db.exec(select(TarjetaNFC).filter(TarjetaNFC.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(TarjetaNFC, "id", tarjeta_id, db=db)
    
@router.delete("/remover/{tarjeta_id}", response_model=TarjetaNFC)
async def remover_tarjeta(tarjeta_id: int, db: SessionDep):
    return crud.remover(TarjetaNFC, "id", tarjeta_id, db)


@router.patch("/actualizar/{tarjeta_id}", response_model=TarjetaNFC)
async def actualizar_tarjeta(tarjeta_id: int, db: SessionDep, nueva_tarjeta: TarjetaNFC):
    return crud.actualizar(TarjetaNFC, tarjeta_id, nueva_tarjeta, db)