#include <Arduino.h>
#line 1 "D:\\MCP_Main\\arduino_builds\\esp32_blink_test_1770041757\\esp32_blink_test_1770041757.ino"

#line 2 "D:\\MCP_Main\\arduino_builds\\esp32_blink_test_1770041757\\esp32_blink_test_1770041757.ino"
void setup();
#line 8 "D:\\MCP_Main\\arduino_builds\\esp32_blink_test_1770041757\\esp32_blink_test_1770041757.ino"
void loop();
#line 2 "D:\\MCP_Main\\arduino_builds\\esp32_blink_test_1770041757\\esp32_blink_test_1770041757.ino"
void setup() {
    Serial.begin(115200);
    pinMode(2, OUTPUT);
    Serial.println("ESP32 Blink Starting");
}

void loop() {
    digitalWrite(2, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    delay(500);
}

