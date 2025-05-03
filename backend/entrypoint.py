from fastapi import FastAPI, Depends
import uvicorn
from config import *
import rutas



app = FastAPI(
    title="API Estudiantes",
    version="0.0.1",
)

iniciar_db()

@app.get("/")
async def hello_check():
    return {
        "msg": "Hola.."
    }


app.include_router(router=rutas.usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(router=rutas.estudiantes.router, prefix="/estudiantes", tags=["estudiantes"])
app.include_router(router=rutas.registro_acceso.router, prefix="/registros", tags=["registros"])
app.include_router(router=rutas.tarjetas.router, prefix="/tarjetas", tags=["tarjetas"])
app.include_router(router=rutas.pagos.router, prefix="/pagos", tags=["pagos"])


if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="0.0.0.0",
                port=8000,
                reload=True)