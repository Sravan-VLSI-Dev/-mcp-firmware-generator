#include <Wire.h>

void setup() {
  Wire.begin();
}

void loop() {
  Wire.beginTransmission(0x48);
  Wire.write(0x55);
  Wire.endTransmission();
  delay(1000); // wait for one second before sending the next byte
}