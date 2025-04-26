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

MFRC522::MIFARE_Key key;

byte block_address = 2; //Bloque de memoria de la tarjeta en que se escribe la cédula.

byte new_block_data[17];

byte buffer_block_size = 18;
byte block_data_read[18];

bool authenticate_keyA() {
  if (mfrc.PCD_Authenticate(0x60, block_address, &key, &(mfrc.uid)) != 0) {
    return false;
  }
  return true;
}

String ReadBlockFromCard() {
    if (!authenticate_keyA()) {
    Serial.println("Key A Authentication failed.");
    return String();
  }

  if (mfrc.MIFARE_Read(block_address, block_data_read, &buffer_block_size) != 0) {
    Serial.println("Read from block 2 failed.");
    return String();
  }

  return String((char *)block_data_read);
}

void printValue() {
  if (!authenticate_keyA()) {
    Serial.println("Key A Authentication failed.");
    return;
  }

  if (mfrc.MIFARE_Read(block_address, block_data_read, &buffer_block_size) != 0) {
    Serial.println("Read from block failed.");
    return;
  }

  Serial.print("Data in block 2: ");
  for (byte i = 0; i < 16; i++) {
    Serial.print((char)block_data_read[i]);
  }
  Serial.println();
}



int8_t WriteCard(String value) {
  value.getBytes(new_block_data, 16);

  if (!authenticate_keyA()) {
    Serial.println("Authentication failed at writing.");
    return -1;
  }

  if (mfrc.MIFARE_Write(block_address, new_block_data, 16) != 0) {
    Serial.println("Write Failed.");
    return -2;
  }

  Serial.println("Data written succesfully in block 2.");
  return 0;
  

}

void InitCardReader() {
  mfrc.PCD_Init();

  for (byte i = 0; i < 6;i++) {
    key.keyByte[i] = 0xFF;
  }
}

//Pausa el lector hasta que se quite la tarjeta actual.
void HaltReader() {
  mfrc.PICC_HaltA();
  mfrc.PCD_StopCrypto1();
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

uint32_t getActualUID() {
  return (actual_uid.integer);
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