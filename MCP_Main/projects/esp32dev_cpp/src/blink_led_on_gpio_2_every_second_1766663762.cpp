#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <SPIFFS.h>

DHT dht;

// Global variables
int ledPin = 2;


void setup() {
  // Initialize LED pin as output
  pinMode(ledPin, OUTPUT);
  
  // Initialize DHT sensor
  dht.pin = 23;
  
  // Initialize I2C communication
  Wire.begin(21, 22);
  
  // Initialize SPIFFS
  SPIFFS.begin(true);
}

void loop() {
  // Read temperature and humidity from DHT sensor
  float temp = dht.getTemperature();
  float humi = dht.getHumidity();
  
  // Blink LED on GPIO 2 every second
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);
}