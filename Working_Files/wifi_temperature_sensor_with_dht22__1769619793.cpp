#include <WiFi.h>
#include <ThingSpeak.h>
#include <Wire.h>
#include <DHT.h>
#include <Adafruit_SSD1306.h>

// Replace with your WiFi credentials
const char* ssid = "your-ssid";
const char* password = "your-password";

// Replace with your ThingSpeak channel ID and API key
long myChannelNumber = 12345;
const char* myWriteAPIKey = "your-write-api-key";

DHT dht(22, DHT22);
WiFiClient client;
Adafruit_SSD1306 display(OLED_SDA, OLED_SCL);

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  
  // Connect to Wi-Fi network with SSID and password
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  
  // Initialize display
  display.begin();
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.println("Connecting to Wi-Fi");
  
  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Current humidity: ");
    Serial.print(h);
    Serial.print("%\t");
    Serial.print("Current temperature: ");
    Serial.print(t);
    Serial.println("°C");
    
    // Upload data to ThingSpeak channel
    int status = ThingSpeak.writeField(myChannelNumber, 1, t, myWriteAPIKey);
    if (status == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.println("Failed to upload data to ThingSpeak channel!");
    }
    
    // Display temperature and humidity on OLED screen
    display.clearDisplay();
    display.setCursor(0, 10);
    display.print("Humidity: ");
    display.println(h);
    display.setCursor(0, 25);
    display.print("Temperature: ");
    display.println(t);
    display.display();
    
    delay(60000); // Update data every 1 minute
  }
}