// This is an example of a malicious sketch that uses the alert() function to execute a JavaScript payload.
// It is not a secure way to use the ESP32, and it is not recommended to use it in a real-world application.

#include <Arduino.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Generate a random number between 0 and 10
  int randNum = random(10);
  
  if (randNum == 7) {
    // Execute the alert() function with the payload "xss"
    Serial.println("<script>alert('xss')</script>");
  }
}