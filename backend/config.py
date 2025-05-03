from sqlmodel import Field, Session, SQLModel, create_engine

#conectar con la base de datos
#url: usuario:contraseña@host:puerto/nombre_base_de_datos
URL_BASE_DE_DATOS = "mysql+pymysql://root:metal2005@localhost:3306/test_tesis2"
engine = create_engine(URL_BASE_DE_DATOS)



def iniciar_db():
    SQLModel.metadata.create_all(engine)

def obtener_db():
    with Session(engine) as db:
        yield db
