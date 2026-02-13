#include <WiFi.h>
#include <ESP32DHT.h>
#include <ThingSpeak.h>
#include <U8g2lib.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

WiFiClient client;
DHT dht(21, DHT22);
ThingSpeak ts(client);
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE, U8X8_PIN_NONE, U8X8_PIN_NONE, U8X8_PIN_NONE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  ledcSetup(0, 5000, 8); // LEDC_CHANNEL_0, frequency=5000Hz, resolution=8 bits
  ledcAttachPin(21, 0); // LEDC_CHANNEL_0, pin=21
  
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();
  
  if (isnan(temp) || isnan(humi)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.println("°C");
    Serial.print("Humidity: ");
    Serial.print(humi);
    Serial.println("%");
    
    ts.begin(client);
    ThingSpeakWriteSuccess writeResult = ts.writeField(1, temp, 0); // Field 1: temperature
    if (writeResult == TS_OK) {
      Serial.println("Temperature data sent successfully.");
    } else {
      Serial.print("Failed to send temperature data: ");
      Serial.println(ts.getLastWriteStatus());
    }
    
    writeResult = ts.writeField(2, humi, 0); // Field 2: humidity
    if (writeResult == TS_OK) {
      Serial.println("Humidity data sent successfully.");
    } else {
      Serial.print("Failed to send humidity data: ");
      Serial.println(ts.getLastWriteStatus());
    }
    
    // Display temperature and humidity on OLED screen
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_helvB10_tf);
    u8g2.drawStr(35, 15, "Temperature:");
    u8g2.drawStr(64, 35, String(temp) + "°C");
    u8g2.setFont(u8g2_font_helvB10_tf);
    u8g2.drawStr(35, 55, "Humidity:");
    u8g2.drawStr(64, 75, String(humi) + "%");
    u8g2.sendBuffer();
    
    delay(30000); // Sleep for 30 seconds before reading again
  }
}