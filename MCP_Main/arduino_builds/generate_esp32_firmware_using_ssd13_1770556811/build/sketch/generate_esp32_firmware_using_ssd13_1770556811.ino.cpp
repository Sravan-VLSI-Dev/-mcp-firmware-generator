#include <Arduino.h>
#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_using_ssd13_1770556811\\generate_esp32_firmware_using_ssd13_1770556811.ino"
#include <Wire.h>
#include <SSD1306.h>

// Define SDA and SCL pins
const int SDA = 21;
const int SCL = 22;

// Define display dimensions
const int DISPLAY_WIDTH = 128;
const int DISPLAY_HEIGHT = 64;

// Define OLED object
SSD1306 display(DISPLAY_WIDTH, DISPLAY_HEIGHT);

void setup() {
  // Initialize Serial communication at 115200 bps
  Serial.begin(115200);

  // Initialize SDA and SCL pins as digital output
  pinMode(SDA, OUTPUT);
  pinMode(SCL, OUTPUT);

  // Initialize OLED display
  display.init();

  // Display "Hello MCP" on the first line of the display
  display.setCursor(0, 0);
  display.println("Hello MCP");

  // Update the uptime in seconds on the second line of the display
  display.setCursor(0, 16);
  display.print("Uptime: ");
  display.print((millis() / 1000));
}

void loop() {
  // Update OLED display with uptime in seconds every second
  if (millis() % 1000 == 0) {
    display.setCursor(0, 16);
    display.print("Uptime: ");
    display.print((millis() / 1000));
  }
}
