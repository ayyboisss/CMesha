#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi Config
const char* ssid = "BHS_MC";
const char* password = "22610esp32";
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

  // Jason where's my information!??!
  StaticJsonDocument<200> doc;
  doc["temperature"] = 23;
  doc["humidity"] = 0.12;
  doc["loudness"] = 47;
  doc["air_quality"] = 250;

  String jsonString;
  serializeJson(doc, jsonString);

  http.begin("http://10.1.34.83:5000/posts");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);

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
  http.end();
}

else{
  Serial.println("There is no connection");
}

delay(5000);  
}
