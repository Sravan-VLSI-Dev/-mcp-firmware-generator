```cpp
#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <SPIFFS.h>

const int BUTTON_PIN = 4;
const int LED_PIN = 2;

void setup() {
  Wire.begin(21, 22);

  dht.pin = 23;

  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == HIGH) {
    ledcSetup(0, 5000, 8);
    ledcAttachPin(LED_PIN, 0);
    ledcWrite(0, 255);
    delay(1000);
    ledcDetachPin(LED_PIN);
    digitalWrite(LED_PIN, LOW);
  }
}
```