scss
#include <WiFi.h>
#include <DHT.h>

// Replace with your Wi-Fi credentials
const char* ssid = "your_ssid";
const char* password = "your_password";

// Replace with the GPIO pin connected to DHT22 sensor
const int dhtPin = 23;

DHT dht(dhtPin, DHT22);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to Wi-Fi...");
    }
    Serial.println("Connected to Wi-Fi");

    ledcSetup(0, 5000, 8); // Set PWM frequency and resolution for channel 0
    ledcAttachPin(LED_BUILTIN, 0); // Attach PWM output to GPIO pin
}

void loop() {
    float temperature = dht.readTemperature();
    Serial.println("Temperature: " + String(temperature));

    ledcWrite(0, map(temperature, 15, 30, 0, 255)); // Map temperature to PWM duty cycle (0-255)
    delay(1000);
}