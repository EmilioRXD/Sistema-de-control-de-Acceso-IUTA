from fastapi import APIRouter, HTTPException, Path, Depends, status, Form
from typing import Any
from config import obtener_db, engine
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
from datetime import date
from rutas.deps import *
from unidecode import unidecode


router = APIRouter()




@router.post("/agregar", dependencies=[UserDep],response_model=Estudiante)
async def registrar_estudiante(request: Estudiante, db: SessionDep) -> Estudiante:
    """Registrar un estudiante al sistema"""
    estudiante = crud.obtener_por_campo(Estudiante, "cedula", request.cedula, db)
    if estudiante is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este estudiante ya existe en el sistema."
        )
    
    estudiante = request
    estudiante.carrera = unidecode(request.carrera).upper()
    
    return crud.añadir(estudiante, db)
    

@router.get("/", dependencies=[UserDep], response_model=List[Estudiante])
async def obtener_estudiantes(db: SessionDep) -> List[Estudiante]:
    """Obtiene todos los estudiantes registrados en el sistema"""
    return crud.obtener_todos(Estudiante, db)


@router.get("/estudiantes_por_carrera", dependencies=[UserDep], response_model=Estudiante)
async def obtener_estudiantes_por_carrera(carrera: str, db: SessionDep):
    """Obtiene los datos del estudiante correspondiente a la cédula"""
    carrera_str = unidecode(carrera).upper()
    query = select(Estudiante).filter(Estudiante.carrera == carrera_str)
    estudiantes = db.exec(query).scalars().all()
    return estudiantes


@router.get("/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def obtener_estudiante_por_cedula(estudiante_cedula: str, db: SessionDep):
    """Obtiene los datos del estudiante correspondiente a la cédula"""
    return crud.obtener_por_campo(Estudiante, "cedula", estudiante_cedula, db=db)


@router.patch("/actualizar/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def actualizar_estudiante(estudiante_cedula: str, db: SessionDep, nuevo_est: Estudiante):
    """Actualizar los datos del estudiante correspondiente a la cédula"""
    return crud.actualizar(Estudiante, estudiante_cedula, nuevo_est, db)



@router.delete("/remover/{estudiante_cedula}", dependencies=[UserDep], response_model=Estudiante)
async def remover_estudiante(estudiante_cedula: str, db: SessionDep):
    """Elimina del sistema el estudiante correspondiente a la cédula"""
    return crud.remover(Estudiante, "cedula", estudiante_cedula, db)


@router.get("/verificar_acceso/{estudiante_cedula}/{tarjeta_id}", dependencies=[KeyDep] ,response_model=AccessResponse)
async def verificar_acceso(estudiante_cedula: str, tarjeta_id: int, db: SessionDep):
    """Toma como entrada la cédula del estudiante y un serial, y verifica que estos esten vinculados en la base de datos.
    Esta función solamente debe ser utilizada por el dispositivo lector mediante una llave de API."""
    estudiante = crud.obtener_por_campo(Estudiante, "cedula", estudiante_cedula, db)
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db)


    if estudiante is None or tarjeta is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante o tarjeta no existe en el sistema.",
        )

    if estudiante.pago_pendiente == False:
        return {"result": False, "detail": "El estudiante no ha cancelado la cuota."}

    #si no coinciden la cedula y serial de la tarjeta con las que estan guardadas en el sistema:
    if estudiante.tarjeta.uid != tarjeta.uid or tarjeta.estudiante_cedula != estudiante_cedula:
        return {"result": False, "detail": "La tarjeta no está vinculada a ningún estudiante."}
    elif tarjeta.activa == False:
        return {"result": False, "detail": "La tarjeta se encuentra inactiva."}
    elif tarjeta.fecha_expiracion < date.today():
        return {"result": False, "detail": "La tarjeta está expirada."}

    return {"result": True, "detail": "Tarjeta verificada correctamente."}