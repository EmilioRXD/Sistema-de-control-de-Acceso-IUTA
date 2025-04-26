#ifndef __ACCESS_CONTROL__
#define __ACCESS_CONTROL__
#include <Arduino.h>

//estructura que guarda el array de bytes y el valor entero
//del UID de la tarjeta 
union UID {
  uint8_t bytes[4];
  uint32_t integer;
};


void printActualUID();
uint32_t getActualUID();
String ReadBlockFromCard();
void HaltReader();
void InitCardReader();
int8_t ScanCards();


#endif //__ACCESS_CONTROL__
