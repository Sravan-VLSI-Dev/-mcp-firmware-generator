#include <DHT.h>

// Define the pin number where the DHT11 is connected
#define DHT_PIN 4

// Initialize the DHT object
DHT dht(DHT_PIN, DHT11);

void setup() {
  // Start serial communication at 115200 baud rate
  Serial.begin(115200);
}

void loop() {
  // Read the temperature and humidity from the DHT sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Print the values to serial monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  // Wait for 2 seconds before reading again
  delay(2000);
}