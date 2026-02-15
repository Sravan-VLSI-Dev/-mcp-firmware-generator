scss
#include <WiFi.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>

const char* ssid = "your_ssid";
const char* password = "your_password";
const char* mqttServer = "your_mqtt_server";
const int mqttPort = 1883;
const char* mqttUsername = "your_username";
const char* mqttPassword = "your_password";

WiFiClient espClient;
MQTTClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  // Connect to MQTT server
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    if (client.connect("ESP32Client", mqttUsername, mqttPassword)) {
      Serial.println("Connected to MQTT server");
    } else {
      Serial.println("Failed to connect to MQTT server");
    }
  }
  
  // Initialize OLED display
  pinMode(14, OUTPUT);
  digitalWrite(14, LOW);
}

void loop() {
  if (client.connected()) {
    client.loop();
    
    // Read temperature from sensor
    float temperature = analogRead(35);
    Serial.println("Temperature: " + String(temperature));
    
    // Publish to MQTT topic
    char payload[64];
    snprintf(payload, sizeof(payload), "{\"temperature\": %f}", temperature);
    client.publish("esp32/temperature", payload);
  } else {
    Serial.println("Not connected to MQTT server");
  }
  
  // Display on OLED display
  displayTemperature(temperature);
}

void displayTemperature(float temperature) {
  // Clear OLED display
  digitalWrite(14, HIGH);
  delay(500);
  digitalWrite(14, LOW);
  
  // Display temperature on OLED display
  Serial.println("Displaying temperature: " + String(temperature));
  oled.print("Temperature: ");
  oled.println(temperature);
}