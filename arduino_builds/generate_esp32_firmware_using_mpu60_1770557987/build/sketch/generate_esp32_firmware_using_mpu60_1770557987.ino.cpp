#include <Arduino.h>
#line 1 "D:\\MCP_Main\\MCP_Main\\arduino_builds\\generate_esp32_firmware_using_mpu60_1770557987\\generate_esp32_firmware_using_mpu60_1770557987.ino"
#include <Wire.h>
#include <MPU6050.h>
#include <SSD1306.h>

// Define I2C pins for MPU6050 and SSD1306 OLED displays
#define MPU_I2C_SDA 21
#define MPU_I2C_SCL 22
#define OLED_I2C_SDA 23
#define OLED_I2C_SCL 24

// Define GPIO pins for buzzer and LED
#define BUZZER_GPIO 25
#define LED_PIN 14

// Initialize MPU6050 sensor with I2C pins
MPU6050 mpu;
Wire.begin(MPU_I2C_SDA, MPU_I2C_SCL);
mpu.initialize();

// Initialize SSD1306 OLED display with I2C pins
SSD1306 oled;
oled.begin(&Wire, OLED_I2C_SDA, OLED_I2C_SCL);

void setup() {
  // Set GPIO pin modes for buzzer and LED
  pinMode(BUZZER_GPIO, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Initialize serial communication at 115200 baud rate
  Serial.begin(115200);
}

void loop() {
  // Read accelerometer data from MPU6050 sensor
  int ax = mpu.readInt(MPU_I2C_SDA, MPU_I2C_SCL);
  int ay = mpu.readInt(MPU_I2C_SDA, MPU_I2C_SCL);
  int az = mpu.readInt(MPU_I2C_SDA, MPU_I2C_SCL);

  // Calculate acceleration magnitude threshold value
  float threshold = 0.5;

  // Check if acceleration magnitude is greater than threshold
  if (sqrt(ax * ax + ay * ay + az * az) > threshold) {
    // Turn buzzer ON and show message on OLED display
    digitalWrite(BUZZER_GPIO, HIGH);
    oled.clear();
    oled.print("FALL DETECTED!");
  } else {
    // Turn buzzer OFF and clear OLED display
    digitalWrite(BUZzer_GPIO, LOW);
    oled.clear();
  }
}
