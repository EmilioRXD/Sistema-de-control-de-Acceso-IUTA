#include <EEPROM.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include "web_portal.h"
#include "access_control.h"
#include <ArduinoJson.h>

#define EEPROM_SIZE 512


Mode driver_mode = MODE_CONFIG;


void setup() {
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE);
  InitCardReader();
  borrarCredenciales();

  bool result = tryConnect();
  if (result) {
    ConnectMQTT();
    driver_mode = MODE_READER;
  }
  else {ESP.restart();}
}


void loop() {
  serverProcess();
  ProcessMQTT();

  switch (driver_mode) {

  case MODE_READER: {
    if (!Cedula().isEmpty() && ScanCards() == 0) {
      printActualUID();
      driver_mode = MODE_WRITER;
    }
    break;
  }
  case MODE_WRITER: {
    if (WriteCard(Cedula()) == 0) {
      printBlock2Data();
      HaltReader();
      driver_mode = MODE_SENDER;
    }
    break;
  }
  case MODE_SENDER: {
    JsonDocument doc; 
    doc["uid"] = getActualUID();
    doc["estudiante_cedula"] = Cedula();

    String jsonResponse;
    serializeJson(doc, jsonResponse); 

    SendDataMQTT(jsonResponse.c_str());

    BorrarCedula();
    delay(2000);
    driver_mode = MODE_READER;
    break;
  }
  case MODE_NONE: {
    break;
  }
  }

}