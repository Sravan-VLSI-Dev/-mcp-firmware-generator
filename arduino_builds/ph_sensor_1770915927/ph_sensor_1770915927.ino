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