from sqlmodel import Field, Session, SQLModel, create_engine

#conectar con la base de datos
URL_BASE_DE_DATOS = "sqlite:///./usuarios.db"
engine = create_engine(URL_BASE_DE_DATOS, connect_args={"check_same_thread": False})



def iniciar_db():
    SQLModel.metadata.create_all(engine)

def obtener_db():
    with Session(engine) as db:
        yield db
