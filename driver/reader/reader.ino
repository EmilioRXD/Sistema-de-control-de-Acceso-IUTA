#include <EEPROM.h>
#include <HTTPClient.h>
#include "web_portal.h"
#include "access_control.h"
#include <ArduinoJson.h>
 
#define EEPROM_SIZE 512

#define LED 2

const String API_KEY = "ESP32-7F3A-9B2E-4D5C";


String server_name = "http://192.168.0.109:8000/estudiantes/verificar_acceso/";

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

  delay(200); digitalWrite(LED, HIGH);
  delay(500); digitalWrite(LED, LOW);

}
//tres veces
void _acceso_denegado() {
  Serial.println("[INFO]: Acceso denegado.");
  for (int i=0;i<3;i++) {
    delay(200); digitalWrite(LED, HIGH);
    delay(200); digitalWrite(LED, LOW);
  }
}


void setup() {
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE);
  pinMode(LED, OUTPUT);
  //borrarCredenciales();

  InitCardReader();

  bool result = tryConnect();
  if (result) {driver_mode = MODE_READER;}
}


void loop() {
  serverProcess();

  if (driver_mode == MODE_READER){
    //si se lee una tarjeta.
    if (ScanCards() == 0) {
      HTTPClient http;
      JsonDocument doc;

      String cedula_tarjeta = ReadBlockFromCard();
      if (cedula_tarjeta.isEmpty()) {cedula_tarjeta = "0";}

                                          //estudiantes/verificar_acceso/cedula/id
      String server_path = server_name + (cedula_tarjeta) + "/" + GetActualUID();
      http.begin(server_path.c_str());
      http.addHeader("api-key", API_KEY);

      int response_code = http.GET();

      if (response_code > 0) {
        Serial.print("HTTP Response code: "); Serial.println(http.errorToString(response_code)); 
        String payload = http.getString();
        deserializeJson(doc, payload.c_str());

        bool permitido = bool(doc["result"]);

        if (permitido) {
          _acceso_permitido();
        }
        else {
          Serial.print("[ERROR]: "); Serial.println(String(doc["detail"]));
          _acceso_denegado();
        }
        
      }
      else {
        Serial.print("Error code: "); Serial.println(response_code);
      }

      HaltReader();
      http.end();
      delay(3000);
    }

  }
  else if (driver_mode == MODE_NONE) {

  }

}
