#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
#include <Arduino.h>

// Pin definitions
#define LED_PIN 2

// Global variables
unsigned long startTime; // Uptime counter
String lastCommand; // Last received command

#line 10 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
void setup();
#line 21 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
void loop();
#line 34 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
void handleCommand(String command);
#line 45 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
void printStatus();
#line 10 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770571486\\generate_esp32_firmware_that_takes__1770571486.ino"
void setup() {
  // Initialize serial communication at 115200 bps
  Serial.begin(115200);
  
  // Setup LED pin as output
  pinMode(LED_PIN, OUTPUT);
  
  // Start uptime counter
  startTime = millis();
}

void loop() {
  // Read incoming serial data
  if (Serial.available()) {
    lastCommand = Serial.readStringUntil('\n');
    
    // Handle command
    handleCommand(lastCommand);
  }
  
  // Print uptime and last command status
  printStatus();
}

void handleCommand(String command) {
  if (command == "LED_ON") {
    digitalWrite(LED_PIN, HIGH);
  } else if (command == "LED_OFF") {
    digitalWrite(LED_PIN, LOW);
  } else {
    // Unknown command, print status
    printStatus();
  }
}

void printStatus() {
  Serial.print("Uptime: ");
  Serial.println(millis() - startTime);
  Serial.print("Last Command: ");
  Serial.println(lastCommand);
}
