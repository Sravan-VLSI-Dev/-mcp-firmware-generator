#include <Arduino.h>
#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\esp32_temperature_sensor_with_mqtt__1770630115\\esp32_temperature_sensor_with_mqtt__1770630115.ino"
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <ESP8266WiFi.h>
#include <MQTTClient.h>
#include <DHTesp.h>

// Define the pins for the DHT11 sensor and OLED display
const int dhtPin = 2;
const int oledSCL = 5;
const int oledSDA = 4;

// Define the MQTT broker connection details
const char* ssid = "your_ssid";
const char* password = "your_password";
const char* mqttServer = "your_mqtt_server";
const char* mqttTopic = "temperature";

// Define the DHT11 sensor object and MQTT client
DHTesp dht;
WiFiClient espClient;
PubSubClient mqtt(espClient);

void setup() {
  Serial.begin(115200);
  
  // Initialize the OLED display
  Adafruit_SSD1306 display = new Adafruit_SSD1306(oledSCL, oledSDA, GEOMETRY_128_64, RGB_COLOR_ORDER);
  
  // Initialize the DHT11 sensor and OLED display
  dht.setup(dhtPin);
  display.begin();
  
  // Connect to WiFi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  // Connect to MQTT broker
  mqtt.setServer(mqttServer, 1883);
}

void loop() {
  // Read the temperature from the DHT11 sensor
  float temp = dht.readTemperature();
  
  // Publish the temperature to the MQTT topic
  if (temp != -127) {
    char message[50];
    snprintf(message, sizeof(message), "%f", temp);
    mqtt.publish(mqttTopic, message);
    
    // Display the temperature on the OLED display
    display.clear();
    display.setTextColor(WHITE, BLACK);
    display.setCursor(0, 0);
    display.println("Temperature: ");
    display.println(temp);
    display.display();
  }
  
  // Delay between temperature reads
  delay(1000);
}
