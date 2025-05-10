from fastapi import APIRouter, HTTPException, Path, Depends, status
from datetime import datetime, timezone, timedelta
from sqlmodel import Session
import rutas.crud as crud
from modelos import *
import json
import time
from typing import Tuple
from rutas.deps import SessionDep
import config
from config import(
    obtener_db,
    engine, 
    mqtt_client as mqtt, 
    conectar_mqtt)

router = APIRouter()



@router.post("/agregar_con_emisor/{cedula_estudiante}")
def agregar_tarjeta_con_emisor(cedula_estudiante: str, db: SessionDep):
    """Al ejecutarse esta función el dispositivo emisor entra en modo de espera hasta que detecta una tarjeta\n
    y escribe la cédula especificada en la tarjeta, vinculandola con el estudiante."""
    estudiante = crud.obtener_por_campo(Estudiante, "cedula", cedula_estudiante, db)
    if estudiante is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No existe un estudiante con la cédula específicada."
        )

   
    counter_start = time.time()
    counter_end = 0

    mqtt.publish("emisor_tarjetas/input", cedula_estudiante)
    #timeout de 10
    while config.mqtt_msg == "" and (counter_end - counter_start < 10):
        counter_end = time.time()

    if config.mqtt_msg == "":
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="No se escaneo la tarjeta dentro del tiempo necesario (10 segundos)."
        )
    
    result = config.mqtt_msg
    config.mqtt_msg = ""

    data = json.loads(result)

    tarjeta = TarjetaNFC(uid=data["uid"],
                         estudiante_cedula=data["estudiante_cedula"],
                         fecha_emision= datetime.now(timezone.utc),
                         fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=365*2),
                         activa=True)
    
    estudiante.tarjeta = tarjeta
    tarjeta.estudiante = estudiante

    db.add(tarjeta)

    db.commit()
    db.refresh(tarjeta)
    db.refresh(estudiante)

    return tarjeta





@router.post("/agregar", response_model=TarjetaNFC)
async def agregar_tarjeta_manualmente(request: TarjetaForm, db: SessionDep) -> TarjetaNFC:
    """Añadir una tarjeta manualmente al sistema si ya se conoce el número de serial."""
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
    
    
@router.get("/tarjetas_total", response_model=List[TarjetaNFC])
async def obtener_tarjetas(db: SessionDep) -> List[TarjetaNFC]:
    """Obtener todas las tarjetas registradas en el sistema."""
    return crud.obtener_todos(TarjetaNFC, db)

@router.get("/tarjetas_por_fecha_de_emision", response_model=List[TarjetaNFC])
async def obtener_tarjetas_por_rango_fecha_de_emision(inicio: date, fin: date ,db: SessionDep) -> List[TarjetaNFC]:
    query = select(TarjetaNFC).filter(TarjetaNFC.fecha_emision > inicio).filter(TarjetaNFC.fecha_emision < fin)
    tarjetas = db.exec(query).scalars().all()
    return tarjetas



@router.delete("/remover/{tarjeta_id}", response_model=TarjetaNFC)
async def remover_tarjeta(tarjeta_id: int, db: SessionDep):
    """Remueve la tarjeta del sistema y elimina los registros de entrada/salida correspondientes a la tarjeta."""
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db)
    db.delete(tarjeta)
    db.commit()
    return tarjeta


@router.patch("/actualizar/{tarjeta_id}", response_model=TarjetaNFC)
async def actualizar_tarjeta(tarjeta_id: int, db: SessionDep, nueva_tarjeta: TarjetaNFC):
    """Actualiza los datos de la tarjeta correspondiente"""
    return crud.actualizar(TarjetaNFC, tarjeta_id, nueva_tarjeta, db)


@router.get("/estudiante/{tarjeta_id}", response_model=Estudiante)
async def obtener_estudiante_por_tarjeta(tarjeta_id: int, db: SessionDep) -> Estudiante:
    """Obtiene los datos del estudiante vinculado a la tarjeta especificada."""
    tarjeta = crud.obtener_por_campo(TarjetaNFC, "uid", tarjeta_id, db)
    return tarjeta.estudiante
