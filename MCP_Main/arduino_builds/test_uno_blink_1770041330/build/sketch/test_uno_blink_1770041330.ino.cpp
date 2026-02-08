#include <Arduino.h>
#line 1 "D:\\MCP_Main\\arduino_builds\\test_uno_blink_1770041330\\test_uno_blink_1770041330.ino"
#line 1 "D:\\MCP_Main\\arduino_builds\\test_uno_blink_1770041330\\test_uno_blink_1770041330.ino"
void setup();
#line 7 "D:\\MCP_Main\\arduino_builds\\test_uno_blink_1770041330\\test_uno_blink_1770041330.ino"
void loop();
#line 1 "D:\\MCP_Main\\arduino_builds\\test_uno_blink_1770041330\\test_uno_blink_1770041330.ino"
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.println("Arduino Uno Blink started");
}

void loop() {
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}

