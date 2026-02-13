#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770854995\\water_level_sensor_1770854995.ino"
#include <Arduino.h>

const int waterLevelPin = 2; // Pin connected to the water level sensor

#line 5 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770854995\\water_level_sensor_1770854995.ino"
void setup();
#line 10 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770854995\\water_level_sensor_1770854995.ino"
void loop();
#line 5 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\water_level_sensor_1770854995\\water_level_sensor_1770854995.ino"
void setup() {
    Serial.begin(115200);
    pinMode(waterLevelPin, INPUT);
}

void loop() {
    int waterLevelValue = analogRead(waterLevelPin);
    Serial.print("Water Level: ");
    Serial.println(waterLevelValue);

    delay(1000); // Read the sensor once per second
}
