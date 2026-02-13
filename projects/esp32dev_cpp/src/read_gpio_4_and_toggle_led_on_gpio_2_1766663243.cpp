#include <Arduino.h>
#include <DHT.h>

DHT dht;

// Global declaration of DHT object


void setup() {
  // Initialize GPIO pin for DHT22 sensor
  dht.pin = 23;

  // Initialize SPIFFS
  SPIFFS.begin(true);

  // Initialize I2C
  Wire.begin(21, 22);

  // Initialize WiFi
  WiFi.begin("SSID", "PASSWORD");
}

void loop() {
  // Read GPIO pin 4 and toggle LED on GPIO 2
  int gpio_state = digitalRead(4);
  if (gpio_state == HIGH) {
    ledcWrite(2, 100);
  } else {
    ledcWrite(2, 0);
  }
}