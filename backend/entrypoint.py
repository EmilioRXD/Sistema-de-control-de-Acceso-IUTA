from fastapi import FastAPI, Depends
from typing import AsyncIterator
from contextlib import asynccontextmanager
import uvicorn
from config import *
import rutas
from rutas import deps


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    try:
        conectar_mqtt()
    except Exception as e:
        print("Error: ", e)

    mqtt_client.subscribe("emisor_tarjetas/output")
    mqtt_client.loop_start()
    yield
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

app = FastAPI(
    title="API Sistema de Control de Acceso",
    version="0.0.1",
    lifespan=lifespan
)

iniciar_db()



@app.get("/")
async def hello_check():
    """Mensaje de Bienvenida"""
    return {
        "msg": "Bienvenido."
    }


app.include_router(router=rutas.usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(router=rutas.estudiantes.router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(router=rutas.registro_acceso.router, prefix="/registros", tags=["Registros"])
app.include_router(router=rutas.tarjetas.router, dependencies=[deps.UserDep], prefix="/tarjetas", tags=["Tarjetas"])
app.include_router(router=rutas.pagos.router, dependencies=[deps.UserDep], prefix="/pagos", tags=["Pagos"])


if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="0.0.0.0",
                port=8000,
                reload=True)