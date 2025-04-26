#include <EEPROM.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "web_portal.h"
#include "access_control.h"
#include <ArduinoJson.h>


#define EEPROM_SIZE 512



enum Mode {
  MODE_CONFIG,
  MODE_READER,
  MODE_WRITER,
  MODE_SENDER,
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


String cedula = "30.998.394";

void loop() {
  serverProcess();

  switch (driver_mode) {

  case MODE_READER: {
    if (ScanCards() == 0) {
      printActualUID();
      driver_mode = MODE_WRITER;
    }
    break;
  }
  case MODE_WRITER: {
    if (WriteCard(cedula) == 0) {
      printValue();
      HaltReader();
      driver_mode = MODE_SENDER;
    }
    break;
  }
  case MODE_SENDER: {
    JsonDocument doc; 
    doc["uid"] = getActualUID();
    doc["estudiante_cedula"] = cedula;
    doc["fecha_emision"] = "2025-04-24";
    doc["fecha_expiracion"] = "2025-04-24";
    doc["activa"] = true;

    String jsonResponse;
    serializeJson(doc, jsonResponse);  // Convertir a String JSON

    Serial.println(jsonResponse);

    HTTPClient http;

    http.begin("192.168.0.109", 8000, "/tarjetas/agregar");

    http.addHeader("Content-Type", "application/json");
    int http_response_code = http.POST(jsonResponse);

    Serial.println(http_response_code);
    String payload = http.getString();
    Serial.println(payload);
    driver_mode = MODE_NONE;
    break;
  }
  case MODE_NONE: {
    //Serial.println("..");
    //sleep(100);
    break;
  }
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