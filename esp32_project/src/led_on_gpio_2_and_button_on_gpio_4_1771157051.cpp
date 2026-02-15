#include <Arduino.h>

const int ledPin = 2; // Pin for LED
const int buttonPin = 4; // Pin for Button

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin to output mode
  pinMode(buttonPin, INPUT_PULLUP); // Set the button pin to input with pull-up resistor
}

void loop() {
  int buttonState = digitalRead(buttonPin); // Read the state of the button
  
  if (buttonState == HIGH) { // If the button is pressed
    digitalWrite(ledPin, HIGH); // Turn on the LED
  } else {
    digitalWrite(ledPin, LOW); // Turn off the LED
  }
}