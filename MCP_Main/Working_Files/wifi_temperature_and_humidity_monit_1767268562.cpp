#include <WiFi.h>
#include <DHT.h>
#include <SPI.h>
#include <Wire.h>
#include <ESP32Servo.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* ssid = "your_ssid";
const char* password = "your_password";
WiFiClient client;

// DHT sensor pin
const int dhtPin = 25;

// ThingSpeak channel ID and read-write API key
String channelID = "your_channel_id";
String readWriteAPIKey = "your_read_write_api_key";

// LED PWM pins
const int ledPin1 = 26;
const int ledPin2 = 27;
const int ledPin3 = 28;

// OLED display pin
const int oledSCL = 4;
const int oledSDA = 5;

void setup() {
  Serial.begin(115200); // Initialize serial port for debugging
  
  // Connect to Wi-Fi network with DHCP
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  // Initialize DHT sensor
  dht.begin();
  
  // Set up LED PWM pins
  ledcSetup(ledPin1, 5000, 8);
  ledcAttachPin(ledPin1, 1);
  ledcSetup(ledPin2, 5000, 8);
  ledcAttachPin(ledPin2, 2);
  ledcSetup(ledPin3, 5000, 8);
  ledcAttachPin(ledPin3, 3);
  
  // Initialize OLED display
  Wire.begin(oledSCL, oledSDA);
  Adafruit_SSD1306 display = Adafruit_SSD1306();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  
  // Print a welcome message on the display
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Welcome to");
  display.println("WiFi Temp/Humidity Monitor");
}

void loop() {
  // Read temperature and humidity from DHT sensor
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Print temperature and humidity on the display
  display.setCursor(0, 20);
  display.println("Temp: " + String(temp) + "C");
  display.println("Humidity: " + String(humidity) + "%");
  
  // Send temperature and humidity data to ThingSpeak channel
  StaticJsonDocument<200> doc;
  doc["field1"] = temp;
  doc["field2"] = humidity;
  char json[200];
  serializeJson(doc, json);
  client.connect("api.thingspeak.com", 80);
  client.println("POST /update HTTP/1.1");
  client.println("Host: api.thingspeak.com");
  client.println("Content-Type: application/x-www-form-urlencoded");
  client.print("X-THINGSPEAKAPIKEY: ");
  client.println(readWriteAPIKey);
  client.print("Content-Length: ");
  client.println(strlen(json));
  client.println();
  client.println(json);
  
  // Set LED PWM duty cycle based on temperature and humidity
  int ledDutyCycle = map(temp, 0, 100, 0, 255);
  ledcWrite(ledPin1, ledDutyCycle);
  
  // Wait for 30 seconds before repeating the loop
  delay(30000);
}