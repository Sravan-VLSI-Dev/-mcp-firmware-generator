#include <Arduino.h>

// constants
const int CHANNEL = 0;
const int RESOLUTION = 8;
const int DUTY_CYCLE = 64; // 25% of 255

void setup() {
  Serial.begin(115200);
  
  // set up LEDC channel 0 with 1kHz frequency and 8-bit resolution
  ledcSetup(CHANNEL, 1000, RESOLUTION);
  
  // attach pin 18 to LEDC channel 0
  ledcAttachPin(18, CHANNEL);
}

void loop() {
  // write duty cycle to LEDC channel 0
  ledcWrite(CHANNEL, DUTY_CYCLE);
  
  // delay for 1 second
  delay(1000);
}