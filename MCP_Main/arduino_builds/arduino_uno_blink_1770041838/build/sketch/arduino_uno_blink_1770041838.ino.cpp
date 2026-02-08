#include <Arduino.h>
#line 1 "D:\\MCP_Main\\arduino_builds\\arduino_uno_blink_1770041838\\arduino_uno_blink_1770041838.ino"

#line 2 "D:\\MCP_Main\\arduino_builds\\arduino_uno_blink_1770041838\\arduino_uno_blink_1770041838.ino"
void setup();
#line 8 "D:\\MCP_Main\\arduino_builds\\arduino_uno_blink_1770041838\\arduino_uno_blink_1770041838.ino"
void loop();
#line 2 "D:\\MCP_Main\\arduino_builds\\arduino_uno_blink_1770041838\\arduino_uno_blink_1770041838.ino"
void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    Serial.println("Arduino Blink Starting");
}

void loop() {
    digitalWrite(13, HIGH);
    delay(1000);
    digitalWrite(13, LOW);
    delay(1000);
}

