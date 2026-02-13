#include <Arduino.h>
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\ph_sensor_1770915927\\ph_sensor_1770915927.ino"
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\ph_sensor_1770915927\\ph_sensor_1770915927.ino"
void setup();
#line 6 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\ph_sensor_1770915927\\ph_sensor_1770915927.ino"
void loop();
#line 1 "C:\\Users\\Tarun Sam\\Library\\Projects\\MCP\\arduino_builds\\ph_sensor_1770915927\\ph_sensor_1770915927.ino"
void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT); //pH sensor pin
}

void loop() {
  int phValue = analogRead(A0);
  float pHLevel = map(phValue, 0, 1023, 0, 14);
  Serial.print("pH Level: ");
  Serial.println(pHLevel);
  delay(1000); // read every second
}
