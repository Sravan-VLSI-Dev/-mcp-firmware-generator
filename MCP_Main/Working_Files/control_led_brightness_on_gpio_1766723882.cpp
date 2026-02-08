#include <Arduino.h>

void setup() {
  // Set up LED PWM at 5000 Hz, 8-bit resolution
  ledcSetup(0, 5000, 8);
  
  // Attach LED to GPIO pin 18
  ledcAttachPin(18, 0);
}

void loop() {
  // Set the LED brightness to 0-255 (255 being full brightness)
  ledcWrite(0, 128);
  
  delay(1000); // Wait for 1 second before changing the LED brightness again
}