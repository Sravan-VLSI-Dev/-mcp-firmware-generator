#include <Arduino.h>
#include <DHT.h>

#define DHTPIN 23 // Define GPIO pin for DHT sensor
#define DHTTYPE DHT22 // Define DHT type as DHT22

DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor

void setup() {
  Serial.begin(115200); // Start serial communication at 115200 baud rate
  while (!Serial) {} // Wait for serial monitor to open
  dht.begin(); // Initialize DHT sensor
}

void loop() {
  float temperature = dht.readTemperature(); // Read temperature from DHT sensor
  float humidity = dht.readHumidity(); // Read humidity from DHT sensor
  if (isnan(temperature) || isnan(humidity)) { // Check if values are valid
    Serial.println("Failed to read from DHT sensor!"); // Print error message
  } else {
    Serial.print("Temperature: "); // Print temperature
    Serial.print(temperature); // Print temperature value
    Serial.print("°C"); // Print degree symbol and C text
    Serial.print("\tHumidity: "); // Print humidity label
    Serial.print(humidity); // Print humidity value
    Serial.println("%"); // Print percentage symbol
  }
  delay(2000); // Wait for 2 seconds before reading again
}