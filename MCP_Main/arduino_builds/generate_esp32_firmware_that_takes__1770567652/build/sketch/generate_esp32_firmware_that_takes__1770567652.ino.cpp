#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770567652\\generate_esp32_firmware_that_takes__1770567652.ino"
#include <Arduino.h>

// Pin definitions
const int LED_PIN = 2;

// Setup function runs once on startup
#line 7 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770567652\\generate_esp32_firmware_that_takes__1770567652.ino"
void setup();
#line 13 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770567652\\generate_esp32_firmware_that_takes__1770567652.ino"
void loop();
#line 7 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_that_takes__1770567652\\generate_esp32_firmware_that_takes__1770567652.ino"
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); // Set LED pin mode to output
}

// Loop function runs repeatedly after setup
void loop() {
  char command;
  
  // Read serial input if available
  if (Serial.available()) {
    command = Serial.read();
    
    switch (command) {
      case 'L': // LED_ON
        digitalWrite(LED_PIN, HIGH);
        break;
        
      case 'l': // LED_OFF
        digitalWrite(LED_PIN, LOW);
        break;
        
      case 'S': // STATUS
        Serial.print("Uptime: ");
        Serial.println(millis());
        Serial.print("Last command: ");
        Serial.println(command);
        break;
    }
  }
}
