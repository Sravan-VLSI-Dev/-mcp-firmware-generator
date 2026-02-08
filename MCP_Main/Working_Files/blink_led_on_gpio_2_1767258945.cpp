#include <Arduino.h>

void setup() {
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    // turn the LED on
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    // turn the LED off
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}