# Backend


## Instrucciones para testear el backend:
1.- Ejecutar mosquitto con el archivo de configuracion en la carpeta backend
para hostear el servidor MQTT
```
mosquitto -c mosquitto.conf
```
2.- Configurar IP en los sketch del ESP:
en reader.ino
```
String server_name = "http://192.168.0.109:8000/estudiantes/verificar_acceso/";
String server_ip = "http://192.168.0.109:8000/";
```
y writer/access_control.cpp
```
const char* SERVER_IP  = "192.168.0.109";
```

3.- Crear una base de datos MySQL y colocar los datos de acceso en el archivo config.py
```
URL_BASE_DE_DATOS = "mysql+pymysql://usuario:contraseña@host:3306/nombre_db"
```

4.- Correr el punto de entrada del backend
```
python3 entrypoint.py
```