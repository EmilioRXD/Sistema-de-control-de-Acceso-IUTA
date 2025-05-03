from typing import *
from pydantic import BaseModel
from sqlalchemy import *
from datetime import date,datetime
from sqlmodel import Field, SQLModel, Relationship


class UsuarioForm(SQLModel):
    nombre: str
    apellido: str
    correo_electronico: str
    contraseña: str

class Token(SQLModel):
    access_token: str
    refresh_token: str

class TokenPayload(SQLModel):
    sub: str = None
    exp: int = None


class AccessResponse(SQLModel):
    result: bool
    detail: str


class Usuario(SQLModel, table=True):
    __tablename__ = "UsuariosAdmin"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo_electronico: str
    contraseña: str

class RegistroAcceso(SQLModel, table=True):
    __tablename__ = "RegistrosAcceso"
    id: Optional[int] = Field(default=None, primary_key=True)
    tarjeta_id: int = Field(default=None, foreign_key="TarjetasNFC.uid")
    tarjeta: Optional["TarjetaNFC"] = Relationship(back_populates="registros")

    fecha_hora_entrada : datetime
    fecha_hora_salida : datetime
    acceso_permitido : bool


class Estudiante(SQLModel, table=True):
    __tablename__ = "Estudiantes"
    cedula: Optional[str] = Field(default=None, primary_key=True)
    nombre : str
    apellido : str
    correo_electronico : str
    telefono : str
    fecha_nacimiento : date
    fecha_registro : datetime

    pagos: List["Pago"] = Relationship(back_populates="estudiante")

    tarjeta: Optional["TarjetaNFC"] = Relationship(back_populates="estudiante",
                                                   sa_relationship_kwargs={"uselist": False})


class Pago(SQLModel, table=True):
    __tablename__ = "Pagos"
    id: Optional[int] = Field(default=None, primary_key=True)

    estudiante_cedula: Optional[str] = Field(default=None, foreign_key="Estudiantes.cedula")
    estudiante: Optional[Estudiante] = Relationship(back_populates="pagos")



class TarjetaForm(SQLModel):
    uid: int
    estudiante_cedula: str


class TarjetaNFC(SQLModel, table=True):
    __tablename__ = "TarjetasNFC"
    uid: int = Field(default=None, primary_key=True)
    estudiante_cedula: Optional[str] = Field(default=None, foreign_key="Estudiantes.cedula")
    fecha_emision: date
    fecha_expiracion: date
    activa: bool

    estudiante: Optional[Estudiante] = Relationship(back_populates="tarjeta")
    registros: List[RegistroAcceso] = Relationship(back_populates="tarjeta")

