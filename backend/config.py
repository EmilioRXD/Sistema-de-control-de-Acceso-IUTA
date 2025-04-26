from sqlmodel import Field, Session, SQLModel, create_engine

#conectar con la base de datos
URL_BASE_DE_DATOS = "postgresql://postgres:postgres@localhost:5432/test"
engine = create_engine(URL_BASE_DE_DATOS)



def iniciar_db():
    SQLModel.metadata.create_all(engine)

def obtener_db():
    with Session(engine) as db:
        yield db
