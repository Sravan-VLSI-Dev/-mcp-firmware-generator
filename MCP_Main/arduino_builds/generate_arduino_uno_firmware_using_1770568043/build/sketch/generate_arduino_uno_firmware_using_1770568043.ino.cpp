#include <Arduino.h>
#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_arduino_uno_firmware_using_1770568043\\generate_arduino_uno_firmware_using_1770568043.ino"
#include <WiFi.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

#line 6 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_arduino_uno_firmware_using_1770568043\\generate_arduino_uno_firmware_using_1770568043.ino"
void setup();
#line 18 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_arduino_uno_firmware_using_1770568043\\generate_arduino_uno_firmware_using_1770568043.ino"
void loop();
#line 6 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_arduino_uno_firmware_using_1770568043\\generate_arduino_uno_firmware_using_1770568043.ino"
void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi network with SSID and password
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Send an HTTP GET request every 5 seconds
  HTTPClient http;
  http.begin("https://example.com/path");
  int httpCode = http.GET();
  if (httpCode == HTTP_CODE_OK) {
    Serial.println("Request sent successfully");
  } else {
    Serial.printf("Error sending request: %d\n", httpCode);
  }
  http.end();

  // Wait for 5 seconds before sending the next request
  delay(5000);
}
