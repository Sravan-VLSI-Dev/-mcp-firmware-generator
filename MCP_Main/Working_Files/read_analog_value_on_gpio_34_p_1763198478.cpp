#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// GPIO pin for reading ADC input
const uint8_t adcPin = 34;

void setup() {
    Serial.begin(115200);
}

void loop() {
    int adcValue = analogRead(adcPin);
    Serial.print("ADC Value: ");
    Serial.println(adcValue);
    delay(1000); // wait for 1 second before reading again
}