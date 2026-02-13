#include <Arduino.h>

void setup() {
    Serial.begin(115200);
}

void loop() {
    static unsigned long previousMillis = 0;
    const long interval = 2000; // Print every 2 seconds
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        Serial.println("Hello World");
        previousMillis = currentMillis;
    }
}