#include <Arduino.h>
#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\build_esp32_firmware_for_smart_stre_1770559793\\build_esp32_firmware_for_smart_stre_1770559793.ino"
#include <Wire.h> // Include Wire library for I2C communication
#include <SSD1306.h> // Include SSD1306 library for OLED display

// Define pin numbers for LDR and LED
const int ldrPin = 34;
const int ledPin = 2;

// Define minimum light level to turn on LED
const int minLightLevel = 500;

// Initialize Wire library for I2C communication
Wire.begin();

// Initialize SSD1306 OLED display
SSD1306 display(0x3c, 4, 5); // Address: 0x3c, SDA: 4, SCL: 5
display.setTextSize(1);
display.setTextColor(WHITE);

void setup() {
  Serial.begin(115200);
  pinMode(ldrPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Read light level from LDR
  int lightLevel = analogRead(ldrPin);

  // Check if light level is below minimum value
  if (lightLevel < minLightLevel) {
    // Turn on LED
    digitalWrite(ledPin, HIGH);

    // Display reading on OLED display
    display.clearDisplay();
    display.print("Light Level: ");
    display.println(lightLevel);
    display.display();
  } else {
    // Turn off LED
    digitalWrite(ledPin, LOW);
  }

  // Delay for a short period to avoid overloading the loop() function
  delay(100);
}
