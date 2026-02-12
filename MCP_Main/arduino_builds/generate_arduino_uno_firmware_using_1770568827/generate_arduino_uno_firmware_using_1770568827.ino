#include <WiFi.h>
#include <ESP32HTTPClient.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  HTTPClient http;
  http.begin("https://example.com/api/data");
  int httpCode = http.GET();
  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    Serial.println(payload);
  } else {
    Serial.print("Error: ");
    Serial.println(http.errorToString(httpCode));
  }
  http.end();
  delay(10000);
}