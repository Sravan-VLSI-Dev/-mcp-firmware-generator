// Blink onboard LED every 1 second using digitalWrite()

#include <Arduino.h>

const int ledPin = 2; // onboard LED pin

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