#include <Arduino.h>
#include <WiFi.h>

// WiFi Config
const char* ssid = "Smart Modem 2-C9L6T8DKJ";
const char* password = "S28BrightJellyfish$";

void setup() {
  Serial.begin(9600);
  delay(2000);

  // WiFi Setup
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
    Serial.println("Still Connecting...");
    delay(2000);
  }

  Serial.println("\nConnecting");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
delay(1000);
}
