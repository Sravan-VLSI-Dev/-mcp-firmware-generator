
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
