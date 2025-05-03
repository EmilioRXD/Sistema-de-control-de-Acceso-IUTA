from fastapi import APIRouter, HTTPException, Path, Depends, status
from datetime import datetime, timezone, timedelta
from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *

router = APIRouter()

SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/agregar", response_model=TarjetaNFC)
async def agregar_tarjeta(request: TarjetaForm, db: SessionDep) -> TarjetaNFC:

    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", request.uid, db)
    if tarjeta is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta tarjeta ya existe en el sistema."
        )

    estudiante = crud.obtener_por_campo(Estudiante, "cedula", request.estudiante_cedula, db)
    if estudiante is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No existe un estudiante con la cédula específicada."
        )
    
    tarjeta = TarjetaNFC(
        uid = request.uid,
        estudiante_cedula=request.estudiante_cedula,
        fecha_emision= datetime.now(timezone.utc),
        fecha_expiracion= datetime.now(timezone.utc) + timedelta(days=365*2), #dos años?
        activa=True
    )
    
    estudiante.tarjeta = tarjeta
    tarjeta.estudiante = estudiante

    db.add(tarjeta)

    db.commit()
    db.refresh(tarjeta)
    db.refresh(estudiante)
    return tarjeta
    
    
@router.get("/", response_model=List[TarjetaNFC])
async def obtener_tarjetas(db: SessionDep) -> List[TarjetaNFC]:
    return crud.obtener_todos(TarjetaNFC, db)


@router.get("/{tarjeta_id}", response_model=TarjetaNFC)
async def obtener_tarjeta_por_id(tarjeta_id: int, db: SessionDep):
    #return db.exec(select(TarjetaNFC).filter(TarjetaNFC.id == usuario_id)).scalars().first()
    return crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db=db)
    

@router.delete("/remover/{tarjeta_id}", response_model=TarjetaNFC)
async def remover_tarjeta(tarjeta_id: int, db: SessionDep):
    return crud.remover(TarjetaNFC, tarjeta_id, db)


@router.patch("/actualizar/{tarjeta_id}", response_model=TarjetaNFC)
async def actualizar_tarjeta(tarjeta_id: int, db: SessionDep, nueva_tarjeta: TarjetaNFC):
    return crud.actualizar(TarjetaNFC, tarjeta_id, nueva_tarjeta, db)


@router.get("/estudiante/{tarjeta_id}", response_model=Estudiante)
async def obtener_estudiante_por_tarjeta(tarjeta_id: int, db: SessionDep) -> Estudiante:
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db)
    return tarjeta.estudiante
