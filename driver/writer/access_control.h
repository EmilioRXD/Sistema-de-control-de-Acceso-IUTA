#ifndef __ACCESS_CONTROL__
#define __ACCESS_CONTROL__
#include <Arduino.h>

//estructura que guarda el array de bytes y el valor entero
//del UID de la tarjeta 
union UID {
  uint8_t bytes[4];
  uint32_t integer;
};


void printValue();
void printActualUID();
uint32_t getActualUID();

void HaltReader();
void InitCardReader();
int8_t ScanCards();
int8_t WriteCard(String Value);


#endif //__ACCESS_CONTROL__
