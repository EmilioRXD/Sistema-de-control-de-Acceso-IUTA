#ifndef __PORTAL_H
#define __PORTAL_H
#include <Arduino.h>


void borrarCredenciales();
bool connectToWiFi();
void serverProcess();
void handleConfig();
void handleRoot();
void handleConnect();

bool tryConnect();

void startCaptivePortal();
void setupWebServer();

#endif //__PORTAL__