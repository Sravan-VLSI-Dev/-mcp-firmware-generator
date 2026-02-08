#include <Arduino.h>

void setup() {
    Serial.begin(115200); // Initialize serial communication at 115200 baud rate
}

void loop() {
    digitalWrite(GPIO_NUM, HIGH); // Turn on LED
    delay(1000); // Wait for 1 second (1000 milliseconds)
    digitalWrite(GPIO_NUM, LOW); // Turn off LED
    delay(1000); // Wait for 1 second (1000 milliseconds)
}