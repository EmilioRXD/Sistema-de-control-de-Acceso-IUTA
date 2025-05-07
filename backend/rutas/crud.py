from fastapi import APIRouter, HTTPException, Path, Depends
from config import obtener_db
from sqlmodel import Session, SQLModel
from modelos import *
from functools import partial
from typing import TypeVar

#crud generico que sirve como base para los routers

Tabla = TypeVar("Tabla")

def añadir(request: Tabla, db: Session) -> SQLModel:
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def obtener_todos(clase: Tabla, db: Session) -> List[SQLModel]:
    return db.exec(select(clase)).scalars().all()

def obtener_por_id(clase: Tabla, id, db: Session) -> SQLModel:
    return db.get(clase, id)

def obtener_por_campo(clase: Tabla, nombre_campo: str, valor_esperado, db: Session) -> SQLModel:
    return db.exec(
        select(clase).filter(clase.__dict__[nombre_campo] == valor_esperado)
        ).scalars().first()



def remover(clase: Tabla, id, db: Session) -> SQLModel:
    obj = obtener_por_id(clase, id, db)
    db.delete(obj)  
    db.commit()
    return obj

def actualizar(clase: Tabla, id, datos_nuevos: SQLModel, db: Session) -> SQLModel:
    obj = obtener_por_id(clase, id, db)
    datos = datos_nuevos.model_dump(exclude_unset=True)
    obj.sqlmodel_update(datos)
    
    db.commit()
    db.refresh(obj)
    return obj