#include <WiFi.h>
#include <DHT.h>
#include <ThingSpeak.h>

// Replace with your WiFi credentials
const char* ssid = "your_ssid";
const char* password = "your_password";

// Replace with your ThingSpeak channel ID and API key
long myChannelNumber = 123456;
const char* myWriteAPIKey = "your_write_api_key";

WiFiClient client;
DHT dht(2, DHT22);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  dht.begin();
}

void loop() {
  int temperature = dht.readTemperature();
  int humidity = dht.readHumidity();
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  ThingSpeak.begin(client);
  int err = ThingSpeak.writeField(myChannelNumber, 1, temperature, myWriteAPIKey);
  if (err == 200) {
    Serial.println("Temperature written successfully.");
  } else {
    Serial.print("Failed to write temperature, error ");
    Serial.print(err);
    Serial.println(". Check your WiFi connection and ThingSpeak channel settings.");
  }
  delay(30000); // Upload data every 30 seconds
}