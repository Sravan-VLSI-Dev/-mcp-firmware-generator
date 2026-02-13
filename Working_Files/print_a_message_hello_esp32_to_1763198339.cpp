#include <Arduino.h>

// Define the GPIO pin numbers for the ESP32 Dev Module
#define LED_PIN    GPIO_NUM_13
#define BUTTON_PIN GPIO_NUM_04

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Print a message to the serial monitor every 2 seconds
  Serial.println("Hello, ESP32!");
  delay(2000);
}