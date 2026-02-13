#include <Arduino.h>
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770909049\\water_level_sensor_1770909049.ino"
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770909049\\water_level_sensor_1770909049.ino"
void setup();
#line 5 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770909049\\water_level_sensor_1770909049.ino"
void loop();
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770909049\\water_level_sensor_1770909049.ino"
void setup() {
  pinMode(4, INPUT); // Water level sensor pin as input
}

void loop() {
  int waterLevel = digitalRead(4);
  Serial.begin(115200);
  if (waterLevel == HIGH) {
    Serial.println("Water Level: High");
  } else if (waterLevel == LOW) {
    Serial.println("Water Level: Low");
  }
}
