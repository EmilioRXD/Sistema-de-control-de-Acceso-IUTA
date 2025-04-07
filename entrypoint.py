from fastapi import FastAPI
import uvicorn
from config import *
from rutas.usuarios import router as router_usuarios
from rutas.estudiantes import router as router_estudiantes




app = FastAPI(
    title="Detalles de Usuarios",
    version="0.0.1"
)

iniciar_db()

@app.get("/")
async def hello_check():
    return {
        "msg": "Hola.."
    }


app.include_router(router=router_usuarios, prefix="/usuarios")
app.include_router(router=router_estudiantes, prefix="/estudiantes")


if __name__ == "__main__":
    uvicorn.run("entrypoint:app",
                host="localhost",
                reload=True)