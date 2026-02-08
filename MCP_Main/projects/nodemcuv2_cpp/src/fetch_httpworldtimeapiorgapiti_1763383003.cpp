#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
}

void loop() {
  HTTPClient http;
  http.begin("http://worldtimeapi.org/api/timezone/Etc/UTC.txt");
  int httpCode = http.GET();
  if (httpCode > 0) {
    String payload = http.getString();
    Serial.println(payload);
  } else {
    Serial.println("Error: " + String(httpCode));
  }
  delay(60000); // wait for 60 seconds before making another request
}