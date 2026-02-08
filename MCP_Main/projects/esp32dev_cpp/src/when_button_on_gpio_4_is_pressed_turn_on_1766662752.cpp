cpp
#include <Arduino.h>
#include <Markruys_DHT.h>
#include <Wire.h>
#include <SPIFFS.h>

// DHT22 sensor on GPIO 14
DHT dht;
dht.pin = GPIO14;

// LED on GPIO 2
int ledPin = 2;

void setup() {
  // Initialize button on GPIO 4 as input with pull-up resistor
  pinMode(4, INPUT_PULLUP);
  
  // Initialize LED on GPIO 2 as output
  pinMode(ledPin, OUTPUT);
  
  // Initialize I2C bus on GPIO 21 and 22
  Wire.begin(21, 22);
  
  // Initialize SPIFFS
  SPIFFS.begin(true);
}

void loop() {
  // Check if button is pressed (HIGH on GPIO 4)
  if (digitalRead(4) == HIGH) {
    // Turn on LED for 1 second
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
  }
}