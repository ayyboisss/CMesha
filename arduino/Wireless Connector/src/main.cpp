#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

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
if (WiFi.status() == WL_CONNECTED){
  HTTPClient http;
  http.begin("http://192.168.1.120:5000/posts");
  int httpResponseCode = http.POST("Testing this from ESP32...");

  if (httpResponseCode > 0){

    String response = http.getString();

    Serial.print("Response Code: ");
    Serial.println(httpResponseCode);
    Serial.print("Response: ");
    Serial.println(response);
  }

  else{
    Serial.println("Something went wrong with the POST request: ");
    Serial.println(httpResponseCode);
  }
}
else{
  Serial.println("There is no connection");
}
delay(5000);  
}
