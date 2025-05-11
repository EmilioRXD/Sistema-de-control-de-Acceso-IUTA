from fastapi import APIRouter, HTTPException, Path, Depends, status
from datetime import datetime, date, time, timedelta
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
        fecha=datetime.now().date(),
        hora=datetime.now().time(),
        tipo=request.tipo,
        acceso_permitido=request.acceso_permitido)
    
    return crud.añadir(registro, db)
    
    
@router.get("/accesos_total", dependencies=[UserDep],response_model=List[RegistroAcceso])
async def obtener_accesos_total(db: SessionDep) -> List[RegistroAcceso]:
    """Obtiene Todos los registros del sistema."""
    return crud.obtener_todos(RegistroAcceso, db)


@router.get("/accesos_por_rango_de_fecha", dependencies=[UserDep], response_model=List[RegistroAcceso])
async def obtener_accesos_por_rango_de_fecha(inicio: str, fin: str, db: SessionDep):
    """Obtiene los accesos entre un rango de fecha. La fecha se especifica en formato Año-mes-dia"""
    inicio_fecha = datetime.strptime(inicio, '%Y-%m-%d').date()
    fin_fecha = datetime.strptime(fin, '%Y-%m-%d').date()

 
    query = select(RegistroAcceso).filter(RegistroAcceso.fecha >= inicio_fecha).filter(RegistroAcceso.fecha <= fin_fecha)
    accesos_fecha = db.exec(query).scalars().all()
    return accesos_fecha

@router.get("/accesos_por_hora", dependencies=[UserDep])
async def obtener_accesos_por_hora(hora: int, db: SessionDep):
    """Obtiene los accesos en una hora especifica. la hora se escribe en formato 24h"""
    hora_rango_menor = time(hora, 0, 0)
    hora_rango_mayor = time(hora+1,0,0)
    query = select(RegistroAcceso).filter(RegistroAcceso.hora > hora_rango_menor).filter(RegistroAcceso.hora < hora_rango_mayor)
    return db.exec(query).scalars().all()



@router.get("/hora_pico", dependencies=[UserDep])
async def obtener_hora_pico_accesos(db: SessionDep):

    query = select(RegistroAcceso).filter(RegistroAcceso.fecha == date.today())
    accesos_hoy = db.exec(query).scalars().all()

    horas = [i.hora for i in accesos_hoy]

    conteo = {}

    for i_hora in horas:
        hora_completa = str(i_hora)
        hora = hora_completa.split(':')[0] + ":00:00"
        conteo[hora] = conteo.get(hora, 0) + 1

    hora_pico = max(conteo.items(), key=lambda x: x[1])
    return hora_pico[0]
     


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
    
