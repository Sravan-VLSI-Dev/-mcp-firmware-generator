#include <ESP32_DHT.h>
#include <WiFi.h>
#include <ThingSpeak.h>

// Replace with your WiFi credentials
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// Replace with your ThingSpeak channel and API key
unsigned long myChannelNumber = YOUR_CHANNEL_NUMBER;
const char* myWriteAPIKey = "YOUR_WRITE_API_KEY";

ESP32_DHT dht(14, DHT11);
WiFiClient client;
ThingSpeakClient thingSpeak(client);

void setup() {
  Serial.begin(115200);
  while (!Serial) { }
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  
  Serial.print("Connected to WiFi");
  
  // Initialize DHT sensor
  dht.begin();
  
  // Initialize ThingSpeak client
  thingSpeak.begin(myChannelNumber, myWriteAPIKey);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if (!isnan(temperature)) {
      ThingSpeakWriteEntry writeEntry = { temperature, humidity };
      thingSpeak.writeMultiple(writeEntry);
      
      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.print("  Humidity: ");
      Serial.println(humidity);
    }
    
    delay(15000); // Wait for 15 seconds before reading again
  } else {
    Serial.print("No WiFi connection");
    delay(1000);
  }
}