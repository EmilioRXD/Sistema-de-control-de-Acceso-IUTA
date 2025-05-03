from fastapi import APIRouter, HTTPException, Path, Depends, status
from typing import Any
from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
from datetime import date
from deps import get_current_user, verify_api_key


router = APIRouter()

KeyDep     = Depends(verify_api_key)
UserDep    = Depends(get_current_user)
SessionDep = Annotated[Session, Depends(obtener_db)]


@router.post("/agregar", response_model=Estudiante)
async def registrar_estudiante(request: Estudiante, db: SessionDep) -> Estudiante: 
    estudiante = crud.obtener_por_campo(Estudiante, "cedula", request.cedula, db)
    if estudiante is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este estudiante ya existe en el sistema."
        )
    
    return crud.añadir(request, db)
    

@router.get("/", dependencies=[UserDep], response_model=List[Estudiante])
async def obtener_estudiantes(db: SessionDep) -> List[Estudiante]:
    return crud.obtener_todos(Estudiante, db)


@router.get("/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def obtener_estudiante_por_cedula(estudiante_cedula: str, db: SessionDep):
    return crud.obtener_por_campo(Estudiante, "cedula", estudiante_cedula, db=db)
    
@router.delete("/remover/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def remover_estudiante(estudiante_cedula: str, db: SessionDep):
    return crud.remover(Estudiante, "cedula", estudiante_cedula, db)


@router.patch("/actualizar/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def actualizar_estudiante(estudiante_cedula: str, db: SessionDep, nuevo_est: Estudiante):
    return crud.actualizar(Estudiante, estudiante_cedula, nuevo_est, db)

@router.get("/tarjeta/{estudiante_cedula}", dependencies=[UserDep], response_model=TarjetaNFC)
async def obtener_tarjeta(estudiante_cedula: str, db: SessionDep) -> TarjetaNFC:
    query = select(TarjetaNFC).filter(TarjetaNFC.estudiante_cedula == estudiante_cedula)
    return db.exec(query).scalars().first()

@router.get("/verificar_acceso/{estudiante_cedula}/{tarjeta_id}", dependencies=[KeyDep] ,response_model=AccessResponse)
async def verificar_acceso(estudiante_cedula: str, tarjeta_id: int, db: SessionDep):
    estudiante = crud.obtener_por_campo(Estudiante, "cedula", estudiante_cedula, db)
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db)


    if estudiante is None or tarjeta is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante o tarjeta no existe en el sistema.",
        )

    #si no coinciden la cedula y serial de la tarjeta con las que estan guardadas en el sistema:
    if estudiante.tarjeta.uid != tarjeta.uid or tarjeta.estudiante_cedula != estudiante_cedula:
        return {"result": False, "detail": "La tarjeta no está vinculada a ningún estudiante."}
    elif tarjeta.activa == False:
        return {"result": False, "detail": "La tarjeta se encuentra inactiva."}
    elif tarjeta.fecha_expiracion < date.today():
        return {"result": False, "detail": "La tarjeta está expirada."}

    return {"result": True, "detail": "Tarjeta verificada correctamente."}