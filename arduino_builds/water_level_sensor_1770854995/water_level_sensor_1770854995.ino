#include <Arduino.h>

const int waterLevelPin = 2; // Pin connected to the water level sensor

void setup() {
    Serial.begin(115200);
    pinMode(waterLevelPin, INPUT);
}

void loop() {
    int waterLevelValue = analogRead(waterLevelPin);
    Serial.print("Water Level: ");
    Serial.println(waterLevelValue);

    delay(1000); // Read the sensor once per second
}