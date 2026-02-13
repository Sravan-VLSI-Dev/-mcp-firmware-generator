#include <Arduino.h>
#line 1 "D:\\MCP_Main\\arduino_builds\\wifi_temperature_sensor_with_dht22__1770089142\\wifi_temperature_sensor_with_dht22__1770089142.ino"
#include <ESP8266WiFi.h>
#include <DHT.h>
#include <ThingSpeak.h>
#include <U8x8lib.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

WiFiClient client;

// DHT22 sensor
DHT dht(14, DHT22);

// ThingSpeak settings
unsigned long myChannelNumber = 12345678;
const char* myWriteAPIKey = "your_write_api_key";

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
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    // Upload temperature and humidity data to ThingSpeak
    ThingSpeak.begin(client);
    int httpCode = ThingSpeak.writeField(myChannelNumber, 1, temperature, myWriteAPIKey);
    if (httpCode == HTTP_CODE_OK) {
      Serial.println("Temperature and humidity data uploaded successfully");
    } else {
      Serial.println("Failed to upload temperature and humidity data to ThingSpeak");
    }
  }

  // Display temperature and humidity on OLED screen
  U8X8_SSD1306_128X64_NONAME_HW_I2C oled;
  oled.begin();
  oled.setCursor(0, 0);
  oled.print("Temperature: ");
  oled.println(temperature);
  oled.setCursor(0, 64 / 8 * 7);
  oled.print("Humidity: ");
  oled.println(humidity);
}
