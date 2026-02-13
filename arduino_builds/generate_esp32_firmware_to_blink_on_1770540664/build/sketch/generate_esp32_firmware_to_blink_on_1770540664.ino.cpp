#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_to_blink_on_1770540664\\generate_esp32_firmware_to_blink_on_1770540664.ino"
// Blink onboard LED every 1 second using digitalWrite()

#include <Arduino.h>

const int ledPin = 2; // onboard LED pin

#line 7 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_to_blink_on_1770540664\\generate_esp32_firmware_to_blink_on_1770540664.ino"
void setup();
#line 12 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_to_blink_on_1770540664\\generate_esp32_firmware_to_blink_on_1770540664.ino"
void loop();
#line 7 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_to_blink_on_1770540664\\generate_esp32_firmware_to_blink_on_1770540664.ino"
void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH);
  delay(1000); // wait for 1 second
  digitalWrite(ledPin, LOW);
  delay(1000); // wait for another 1 second
}
