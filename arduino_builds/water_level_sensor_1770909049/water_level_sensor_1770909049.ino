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