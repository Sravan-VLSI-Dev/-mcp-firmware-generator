void setup() {
  Serial.begin(115200);
  
  // Initialize pin as output for LED indicator
  pinMode(LED_BUILTIN, OUTPUT);

  // Initialize pin as input for water level sensor (e.g. analog pin)
  pinMode(A0, INPUT);
}

void loop() {
  int sensorValue = analogRead(A0); // Read the water level sensor value

  if(sensorValue > 100) { // Define your threshold here
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED indicator when water level is high
  } else {
    digitalWrite(LED_BUILTIN, LOW); // Turn off LED indicator when water level is low
  }
  
  delay(500); // Adjust the sampling rate as needed
}