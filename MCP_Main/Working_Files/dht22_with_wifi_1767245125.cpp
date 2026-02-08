#include <WiFi.h>
#include <DHT.h>

// Define the GPIO pin connections for the DHT22 sensor
#define DHTPIN 14  // Data pin for the DHT22 sensor
#define DHTTYPE DHT22   // Sensor type (DHT22)

// Set up the WiFi connection
const char* ssid = "your_ssid"; // SSID of your WiFi network
const char* password = "your_password"; // Password for your WiFi network
WiFiClient client;

// Set up the DHT22 sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  
  // Connect to the WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  // Initialize the DHT22 sensor
  dht.begin();
}

void loop() {
  // Read the temperature and humidity from the DHT22 sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // Convert the temperature and humidity values to strings
  String temperatureStr = String(temperature);
  String humidityStr = String(humidity);
  
  // Send a HTTP POST request to a server with the temperature and humidity values
  client.post("http://your_server_ip/weather", "{\"temperature\":\"" + temperatureStr + "\", \"humidity\":\"" + humidityStr + "\"}");
  
  // Delay between readings
  delay(1000);
}