#include <Arduino.h>

const int BUTTON_PIN = 8;
const int LED_PIN = 13;
int lastButtonState = LOW;

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int buttonState = digitalRead(BUTTON_PIN);
  if (buttonState != lastButtonState) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
  lastButtonState = buttonState;
}