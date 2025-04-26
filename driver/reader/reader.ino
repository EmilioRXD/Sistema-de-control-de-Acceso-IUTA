#include <EEPROM.h>
#include <HTTPClient.h>
#include "web_portal.h"
#include "access_control.h"
#include <ArduinoJson.h>
 
#define EEPROM_SIZE 512


String server_name = "http://192.168.0.109:8000/estudiantes/tarjeta/";

enum Mode {
  MODE_CONFIG,
  MODE_READER,
  MODE_NONE
};

Mode driver_mode = MODE_CONFIG;


void setup() {
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE);
  InitCardReader();

  bool result = tryConnect();
  if (result) {driver_mode = MODE_READER;}
  else {ESP.restart();}
}




void loop() {
  serverProcess();

  if (driver_mode == MODE_READER){
    if (ScanCards() == 0) {
      String cedula_tarjeta = ReadBlockFromCard();
      String cedula_recibida;

      String server_path = server_name + (cedula_tarjeta);
      JsonDocument doc;

      HTTPClient http;

      http.begin(server_path.c_str());

      int response_code = http.GET();

      if (response_code>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(response_code);
        String payload = http.getString();

        deserializeJson(doc, payload.c_str());

        Serial.println(bool(doc["activa"]));
      }
      else {
        Serial.print("Error code: ");
        Serial.println(response_code);
      }



      

      http.end();
      HaltReader();
    }

  }
  else if (driver_mode == MODE_NONE) {

  }

}

/*
void scan() {
    HTTPClient http;
    if (!http.begin("192.168.0.109", 8000, "/usuarios/")) {
      Serial.println("[ERROR] Unable to connect.");
    }

    int response_code = http.GET();

    if (response_code > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(response_code);
        String payload = http.getString();
        Serial.println(payload);
    }
    else {
        Serial.print("Error code: ");
        Serial.println(response_code);
    }
}
*/