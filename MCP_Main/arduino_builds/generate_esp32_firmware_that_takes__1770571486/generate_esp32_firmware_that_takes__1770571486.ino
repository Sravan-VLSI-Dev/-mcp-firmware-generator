#include <Arduino.h>

// Pin definitions
#define LED_PIN 2

// Global variables
unsigned long startTime; // Uptime counter
String lastCommand; // Last received command

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