#include <EEPROM.h>
#include <HTTPClient.h>
#include "web_portal.h"
#include "access_control.h"
 

#define EEPROM_SIZE 512



enum Mode {
  MODE_CONFIG,
  MODE_READER
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
      HaltReader();
      printActualUID();
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