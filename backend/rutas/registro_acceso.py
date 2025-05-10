from fastapi import APIRouter, HTTPException, Path, Depends, status
from datetime import datetime, date, time
from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
from rutas.deps import *

router = APIRouter()




#este metodo idealmente solo debe ser ejecutado por el dispositivo lector
@router.post("/agregar", dependencies=[KeyDep], response_model=RegistroAcceso)
async def agregar_registro(request: RegistroForm, db: SessionDep) -> RegistroAcceso:
    """Agrega un registro de entrada/salida al sistema.\n
    Esta funcion solo debe ser llamada por el dispositivo lector."""

    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", request.tarjeta_id, db)
    if tarjeta is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarjeta con esta ID no existe."
        )

    registro = RegistroAcceso(
        tarjeta_id=request.tarjeta_id,
        tarjeta=tarjeta,
        fecha_hora=datetime.now(),
        tipo=request.tipo,
        acceso_permitido=request.acceso_permitido)
    
    return crud.añadir(registro, db)
    
    
@router.get("/accesos_total", dependencies=[UserDep],response_model=List[RegistroAcceso])
async def obtener_accesos_total(db: SessionDep) -> List[RegistroAcceso]:
    """Obtiene Todos los registros del sistema."""
    return crud.obtener_todos(RegistroAcceso, db)


@router.get("/accesos_por_rango_de_fecha", dependencies=[UserDep], response_model=int)
async def obtener_accesos_por_rango_de_fecha(inicio: date, fin: date, db: SessionDep) -> int:
    query = select(RegistroAcceso).filter(RegistroAcceso.fecha_hora.date() > inicio).filter(RegistroAcceso.fecha_hora.date() < fin)
    accesos_fecha = db.exec(query).scalars().all()
    return accesos_fecha




@router.get("/hora_pico", dependencies=[UserDep], response_model=time)
async def obtener_hora_pico_accesos(db: SessionDep) -> time:
    query = select(RegistroAcceso).filter(RegistroAcceso.fecha_hora.date() == date.today())
    accesos_hoy = db.exec(query).scalars().all()
     


@router.get("/{estudiante_cedula}", dependencies=[UserDep], response_model=List[RegistroAcceso])
async def obtener_accesos_de_estudiante(estudiante_cedula: str, db: SessionDep):
    """Obtiene todos los registros de entrada/salida de un estudiante"""
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "estudiante_cedula", estudiante_cedula, db)

    if tarjeta is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El Estudiante no tiene una tarjeta asignada."
        )

    query = select(RegistroAcceso).where(RegistroAcceso.tarjeta_id == tarjeta.uid)
    return db.exec(query).scalars().all()

@router.get("/{registro_id}", dependencies=[UserDep],response_model=RegistroAcceso)
async def obtener_registro_por_id(registro_id: int, db: SessionDep):
    return crud.obtener_por_campo(RegistroAcceso, "id", registro_id, db=db)
    
