#include <Arduino.h>

// Define GPIO pin for LED
const int ledPin = 2;

void setup() {
    // Set GPIO 2 as output
    pinMode(ledPin, OUTPUT);
}

void loop() {
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
}