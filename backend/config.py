from sqlmodel import Field, Session, SQLModel, create_engine
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish

#conectar con la base de datos
#url: usuario:contraseña@host:puerto/nombre_base_de_datos
URL_BASE_DE_DATOS = "mysql+pymysql://root:metal2005@localhost:3306/test_tesis"
engine = create_engine(URL_BASE_DE_DATOS)

mqtt_msg = ""

def message_handle_callback(client, userdata, msg):
    global mqtt_msg
    #print(f"{msg.topic}: {msg.payload.decode()}")
    mqtt_msg = msg.payload.decode()



#Cliente mqtt
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="f-backend", clean_session=False)
mqtt_client.on_message = message_handle_callback


DIRECCION_HOST = "0.0.0.0"
MQTT_PUERTO = 1884



def conectar_mqtt():
    if mqtt_client.connect(DIRECCION_HOST, MQTT_PUERTO, 60) != 0:
        raise Exception("No se pudo conectar al cliente MQTT, Inicie un servidor en el puerto 1884")



def iniciar_db():
    SQLModel.metadata.create_all(engine)

def obtener_db():
    with Session(engine) as db:
        yield db
