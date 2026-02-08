#include <WiFi.h>
#include <DHTesp.h>

// D5 and D6 are used as pins for the sensor and data transmission
const int temperatureSensorPin = 14; // D5
const int dataTransmissionPin = 12; // D6

// Set up the WiFi module and configure it to connect to a network
WiFiEspServer server(80); // Create an instance of the WiFi server on port 80
String ssid = "my_ssid"; // Your WiFi network's SSID
String password = "my_password"; // Your WiFi network's password

void setup() {
  Serial.begin(115200); // Initialize serial communication at a speed of 115200 bps
  Serial.println("Starting up...");

  // Initialize the DHT sensor on pin 14 (D5)
  DHTesp.setup(temperatureSensorPin, DHTesp::DHT22);

  // Connect to WiFi network with SSID and password
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // Start the server on port 80
  server.begin();
}

void loop() {
  // Check if a client has connected to the server
  WiFiEspClient client = server.available();
  if (client) {
    Serial.println("New client connected.");

    // Read data from the sensor and send it back to the client as HTML
    float temperature = DHTesp.readTemperature(true); // Read the temperature in Celsius with a resolution of 1 decimal place
    String html = "<html><body>Temperature: " + String(temperature) + " degrees Celsius</body></html>";
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println(html);

    // Close the connection with the client
    client.stop();
  }
}