#include <EEPROM.h>
#include <HTTPClient.h>
#include "web_portal.h"
#include "access_control.h"
#include <ArduinoJson.h>
 
#define EEPROM_SIZE 512

#define LED 2


String server_name = "http://192.168.0.109:8000/estudiantes/tarjeta/";

enum Mode {
  MODE_CONFIG,
  MODE_READER,
  MODE_NONE
};

Mode driver_mode = MODE_CONFIG;

//funciones de prueba

//una vez
void _acceso_permitido() {
  Serial.println("[INFO]: Acceso permitido.");

  delay(200);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);

}
//tres veces
void _acceso_denegado() {
  Serial.println("[INFO]: Acceso denegado.");
  for (int i=0;i<3;i++) {
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
  }
}


void setup() {
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE);
  pinMode(LED, OUTPUT);

  InitCardReader();

  bool result = tryConnect();
  if (result) {driver_mode = MODE_READER;}
  else {ESP.restart();}
}




void loop() {
  serverProcess();

  if (driver_mode == MODE_READER){
    //si se lee una tarjeta.
    if (ScanCards() == 0) {
      HTTPClient http;
      JsonDocument doc;

      String cedula_tarjeta = ReadBlockFromCard();

      //GET que recibe la cédula vinculada al UID de la tarjeta
      String server_path = server_name + (cedula_tarjeta);
      http.begin(server_path.c_str());
      int response_code = http.GET();

      if (response_code > 0) {
        Serial.print("HTTP Response code: "); Serial.println(response_code);
        String payload = http.getString();
        deserializeJson(doc, payload.c_str());

        bool tarjeta_activa = bool(doc["activa"]);
        uint32_t uid = uint32_t(doc["uid"]);

        //verifíca que la UID vinculada al estudiante en la base de datos
        //sea la misma que la UID que se está leyendo
        if (tarjeta_activa && uid == GetActualUID()) {
          _acceso_permitido();
        }
        else {
          _acceso_denegado();
        }
        
      }
      else {
        Serial.print("Error code: "); Serial.println(response_code);
      }

      http.end();
      HaltReader();
    }

  }
  else if (driver_mode == MODE_NONE) {

  }

}
