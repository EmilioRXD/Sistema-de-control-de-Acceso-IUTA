#include <cstdint>
#include "access_control.h"
#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
//#include <MFRC522DriverI2C.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>

#define SS_PIN 21

static UID actual_uid;

MFRC522DriverPinSimple ss_pin(SS_PIN); 

MFRC522DriverSPI driver{ss_pin};//spi driver
MFRC522 mfrc{driver}; //class instance


void InitCardReader() {
  mfrc.PCD_Init();
}

//Pausa el lector hasta que se quite la tarjeta actual.
void HaltReader() {
  mfrc.PICC_HaltA();
}


void printActualUID() {
  Serial.print("\nHEX:");
  for (uint8_t i = 0; i < 4;i++) {
    Serial.print(actual_uid.bytes[i] < 0x10 ? " 0" : " ");
    Serial.print(actual_uid.bytes[i], HEX);   
  }
  Serial.println();
  Serial.print("INT: "); Serial.println(actual_uid.integer);
}


//Regresa:
//-1 si no hay tarjetas presentes.
//-2 si no se pudo leer la tarjeta.
//0 si se leyó la tarjeta.
int8_t ScanCards() {
  if (!mfrc.PICC_IsNewCardPresent())
   return -1;

  if (!mfrc.PICC_ReadCardSerial())
    return -2;

  for (byte i = 0; i < mfrc.uid.size;i++) {
    actual_uid.bytes[i] = mfrc.uid.uidByte[i];
  }
  //printActualUID();
  return 0;
  
}