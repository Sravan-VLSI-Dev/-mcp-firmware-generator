#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <SSD1306.h>

// Wifi credentials
const char* ssid = "your_ssid";
const char* password = "your_password";

// ThingSpeak channel ID and API key
long channelID = 12345;
String apiKey = "your_api_key";

// DHT sensor settings
#define DHTPIN 21 // GPIO pin for DHT22/AM2302 data line (must be a hardware interrupt pin)
#define DHTTYPE DHT22 // DHT22 or AM2302 sensor
DHT dht(DHTPIN, DHTTYPE);

// OLED display settings
SSD1306 display(0x3c, 4, 5); // Address, SCLK pin, MOSI pin

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  // Initialize DHT sensor
  dht.begin();
  
  // Initialize OLED display
  display.init();
}

void loop() {
  // Read temperature and humidity from DHT sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Check if readings are valid, if not retry until they are
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(1000);
    return;
  }
  
  // Display temperature and humidity on OLED screen
  display.clear();
  display.setCursor(0, 0);
  display.print("Temperature: ");
  display.println(temperature);
  display.setCursor(0, 16);
  display.print("Humidity: ");
  display.println(humidity);
  
  // Upload readings to ThingSpeak
  HTTPClient http;
  http.begin("https://api.thingspeak.com/update");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  String data = "api_key=" + apiKey + "&field1=" + temperature + "&field2=" + humidity;
  int httpCode = http.POST(data);
  
  if (httpCode > 0) {
    Serial.print("HTTP code: ");
    Serial.println(httpCode);
  } else {
    Serial.println("Failed to upload data!");
  }
  
  // Delay between reads
  delay(300000);
}