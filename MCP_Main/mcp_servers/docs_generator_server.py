#!/usr/bin/env python3
"""
Documentation Generator Server - Auto-generate professional docs
Phase 7: Optional documentation enhancement
"""

import json
import os
import re
from typing import Dict, List, Optional
from datetime import datetime

class DocsGeneratorServer:
    """Generate professional documentation for embedded code."""
    
    def __init__(self, host: str = None, model: str = None):
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11435")
        self.model = model or os.getenv("OLLAMA_MODEL", "codellama")
        # Ollama client is optional - only needed for advanced features
        try:
            import ollama
            self.client = ollama.Client(host=self.host)
            self.has_ollama = True
        except ImportError:
            self.client = None
            self.has_ollama = False
    
    def extract_hardware_info(self, code: str) -> Dict:
        """Extract hardware information from code."""
        
        info = {
            "includes": [],
            "gpio_usage": [],
            "protocols": [],
            "sensors": [],
            "actuators": []
        }
        
        # Extract includes
        includes = re.findall(r'#include\s+[<"]([^>"]+)[>"]', code)
        info["includes"] = includes
        
        # Detect protocols
        if "Wire.begin" in code or "Wire.h" in code:
            info["protocols"].append("I2C")
        if "SPI.begin" in code or "SPI.h" in code:
            info["protocols"].append("SPI")
        if "Serial.begin" in code:
            info["protocols"].append("UART")
        if "WiFi" in code:
            info["protocols"].append("WiFi")
        if "BLE" in code or "Bluetooth" in code:
            info["protocols"].append("Bluetooth/BLE")
        if "MQTT" in code or "PubSubClient" in code:
            info["protocols"].append("MQTT")
        
        # Detect common sensors
        sensor_map = {
            "DHT": "Temperature/Humidity Sensor (DHT22/DHT11)",
            "BMP": "Pressure Sensor (BMP180/BMP280)",
            "MPU": "IMU/Accelerometer (MPU6050)",
            "ADS": "ADC Converter (ADS1115)",
            "MQ": "Gas Sensor (MQ series)",
            "DS18": "Temperature Sensor (DS18B20)",
            "ADXL": "Accelerometer (ADXL345)",
            "TMP": "Temperature Sensor (TMP36)",
            "HC-SR04": "Ultrasonic Distance Sensor",
            "PIR": "Motion Sensor (PIR)"
        }
        
        for key, sensor in sensor_map.items():
            if key in code:
                info["sensors"].append(sensor)
        
        # Detect actuators
        actuator_map = {
            "digitalWrite.*LOW": "LED/Digital Output",
            "ledcWrite": "PWM Output",
            "Servo": "Servo Motor",
            "analogWrite": "Analog/PWM Output",
            "Motor": "DC Motor"
        }
        
        for key, actuator in actuator_map.items():
            if re.search(key, code):
                if actuator not in info["actuators"]:
                    info["actuators"].append(actuator)
        
        # Extract GPIO pins
        gpio_patterns = [
            r'(?:GPIO|Pin|gpio)\s*[=:]\s*(\d+)',
            r'const\s+(?:int|byte|uint8_t)\s+\w+\s*=\s*(\d+)',
            r'#define\s+\w+\s+(\d+)'
        ]
        pins = []
        for pattern in gpio_patterns:
            pins.extend(re.findall(pattern, code, re.IGNORECASE))
        info["gpio_usage"] = sorted(list(set(pins)))
        
        return info
    
    def generate_hardware_guide(self, code: str, description: str) -> str:
        """Generate hardware setup guide."""
        
        hardware_info = self.extract_hardware_info(code)
        
        guide = f"""# Hardware Setup Guide

## Project: {description}

## Overview
This project uses the following hardware components and protocols.

## Hardware Components

### Microcontroller
- ESP32 DevKit V1 (or compatible)
- Operating Voltage: 3.3V
- Input Voltage: 5V via USB or 7-12V via VIN

### Sensors
"""
        
        if hardware_info["sensors"]:
            for sensor in hardware_info["sensors"]:
                guide += f"- {sensor}\n"
        else:
            guide += "- No external sensors detected\n"
        
        guide += "\n### Actuators/Outputs\n"
        if hardware_info["actuators"]:
            for actuator in hardware_info["actuators"]:
                guide += f"- {actuator}\n"
        else:
            guide += "- No actuators detected\n"
        
        guide += "\n### Communication Protocols\n"
        if hardware_info["protocols"]:
            for protocol in hardware_info["protocols"]:
                guide += f"- {protocol}\n"
        else:
            guide += "- No external protocols detected\n"
        
        guide += "\n### Additional Components Needed\n"
        guide += "- USB cable (for programming and power)\n"
        guide += "- Breadboard and jumper wires\n"
        if "I2C" in hardware_info["protocols"]:
            guide += "- Pull-up resistors (2x 4.7kΩ) for I2C\n"
        guide += "- Capacitors (0.1µF ceramic) for power filtering\n"
        
        return guide
    
    def generate_pin_guide(self, code: str) -> str:
        """Generate pin configuration guide."""
        
        guide = "# Pin Configuration\n\n"
        guide += "## GPIO Pins Used in This Project\n\n"
        
        # Extract pin assignments with variable names
        pin_patterns = [
            (r'const\s+(?:int|byte|uint8_t)\s+(\w+)\s*=\s*(\d+)', 'const declaration'),
            (r'#define\s+(\w+)\s+(\d+)', '#define directive')
        ]
        
        all_pins = []
        for pattern, source in pin_patterns:
            matches = re.findall(pattern, code)
            all_pins.extend([(var, pin, source) for var, pin in matches])
        
        if all_pins:
            guide += "| Variable Name | GPIO Pin | Source |\n"
            guide += "|---------------|----------|--------|\n"
            for var, pin, source in all_pins:
                guide += f"| {var} | GPIO{pin} | {source} |\n"
        else:
            guide += "No explicit pin assignments found.\n"
        
        # Add common ESP32 pins reference
        guide += "\n## ESP32 DevKit V1 Pin Reference\n\n"
        guide += """| Function | GPIO | Notes |
|----------|------|-------|
| Boot Button | 0 | Pull-up required, used for boot mode |
| TX (UART0) | 1 | Serial output (avoid using if using Serial) |
| Built-in LED | 2 | Active LOW on most boards |
| RX (UART0) | 3 | Serial input (avoid using if using Serial) |
| SDA (I2C) | 21 | Default I2C data line |
| SCL (I2C) | 22 | Default I2C clock line |
| MOSI (SPI) | 23 | SPI master out, slave in |
| MISO (SPI) | 19 | SPI master in, slave out |
| SCK (SPI) | 18 | SPI clock |
| SS (SPI) | 5 | SPI chip select |
| ADC1 Pins | 32-39 | Analog input capable |
| DAC Pins | 25, 26 | Digital-to-analog capable |
| Touch Pins | 0,2,4,12-15,27,32,33 | Capacitive touch sensing |
| GND | GND | Ground reference |
| 3.3V | 3V3 | 3.3V output (max 600mA) |
| 5V | 5V/VIN | 5V input/output |

**⚠️ CAUTION:**
- GPIO 6-11 are used for internal flash - DO NOT USE
- GPIO 34-39 are input only (no pull-up/pull-down)
- All GPIO pins are 3.3V - NOT 5V tolerant!
"""
        
        guide += "\n## Wiring Best Practices\n\n"
        guide += "1. **I2C Connections:** Always use 4.7kΩ pull-up resistors on SDA and SCL\n"
        guide += "2. **Power Decoupling:** Add 0.1µF capacitors near sensor VCC/GND pins\n"
        guide += "3. **Wire Length:** Keep sensor wires under 30cm for reliable I2C\n"
        guide += "4. **Breadboard:** Use quality breadboards with good connections\n"
        guide += "5. **Polarity:** Double-check VCC/GND before powering on\n"
        guide += "6. **Current Limiting:** Add resistors to LEDs (220Ω-1kΩ)\n"
        guide += "7. **Level Shifting:** Use level shifters for 5V sensors\n"
        
        return guide
    
    def generate_library_guide(self, code: str, libraries: List[str]) -> str:
        """Generate library installation guide."""
        
        guide = "# Library Installation Guide\n\n"
        guide += "## Required Libraries\n\n"
        
        # Filter out built-in libraries
        builtin_libs = ["Arduino.h", "Wire.h", "SPI.h", "WiFi.h", "Serial.h", 
                       "EEPROM.h", "FS.h", "SPIFFS.h", "LittleFS.h"]
        external_libs = [lib for lib in libraries if lib not in builtin_libs]
        
        if external_libs:
            guide += f"This project requires **{len(external_libs)}** external libraries.\n\n"
            
            guide += "### Method 1: PlatformIO CLI (Recommended)\n\n"
            guide += "Open terminal in project directory and run:\n\n"
            guide += "```bash\n"
            for lib in external_libs:
                guide += f'pio lib install "{lib}"\n'
            guide += "```\n\n"
            
            guide += "### Method 2: PlatformIO IDE\n\n"
            guide += "1. Open PlatformIO sidebar → Libraries\n"
            guide += "2. Search and install each library:\n"
            for i, lib in enumerate(external_libs, 1):
                guide += f"   {i}. Search: `{lib.split('/')[-1]}`\n"
            guide += "3. Click **Install** for each\n"
            guide += "4. Restart IDE\n\n"
            
            guide += "### Method 3: platformio.ini Configuration\n\n"
            guide += "Add these lines to your `platformio.ini`:\n\n"
            guide += "```ini\n"
            guide += "[env:esp32dev]\n"
            guide += "platform = espressif32\n"
            guide += "board = esp32dev\n"
            guide += "framework = arduino\n"
            guide += "lib_deps =\n"
            for lib in external_libs:
                guide += f"    {lib}\n"
            guide += "```\n\n"
            
            guide += "PlatformIO will auto-install libraries on first build.\n"
        else:
            guide += "✅ **Good news!** This project uses only built-in Arduino libraries.\n\n"
            guide += "No external library installation required. You can compile immediately.\n"
        
        guide += "\n### Built-in Libraries Used\n\n"
        builtin_used = [lib for lib in libraries if lib in builtin_libs]
        if builtin_used:
            for lib in builtin_used:
                guide += f"- `{lib}` (Arduino Core)\n"
        
        return guide
    
    def generate_code_walkthrough(self, code: str) -> str:
        """Generate code walkthrough."""
        
        walkthrough = "## Code Walkthrough\n\n"
        walkthrough += "### Program Structure\n\n"
        
        # Analyze setup() function
        if "void setup()" in code:
            walkthrough += "#### `void setup()`\n"
            walkthrough += "Runs **once** when the board powers on or resets.\n\n"
            walkthrough += "**Initialization tasks:**\n"
            
            if "Serial.begin" in code:
                walkthrough += "- ✓ Initialize serial communication for debugging\n"
            if "pinMode" in code:
                walkthrough += "- ✓ Configure GPIO pin modes (INPUT/OUTPUT)\n"
            if "WiFi.begin" in code:
                walkthrough += "- ✓ Connect to WiFi network\n"
            if "Wire.begin" in code:
                walkthrough += "- ✓ Initialize I2C bus\n"
            if "SPI.begin" in code:
                walkthrough += "- ✓ Initialize SPI bus\n"
            if ".begin()" in code:
                walkthrough += "- ✓ Initialize sensors/peripherals\n"
            
            walkthrough += "\n"
        
        # Analyze loop() function
        if "void loop()" in code:
            walkthrough += "#### `void loop()`\n"
            walkthrough += "Runs **continuously** after setup() completes.\n\n"
            walkthrough += "**Main program flow:**\n"
            
            if "read" in code.lower():
                walkthrough += "1. Read sensor data\n"
            if "print" in code.lower():
                walkthrough += "2. Output data to Serial\n"
            if "publish" in code.lower() or "send" in code.lower():
                walkthrough += "3. Send data over network\n"
            if "digitalWrite" in code:
                walkthrough += "4. Control output devices\n"
            if "delay" in code:
                walkthrough += "5. Wait before next iteration\n"
            
            walkthrough += "\n"
        
        # Find custom functions
        custom_functions = re.findall(r'(?:void|int|float|bool|String)\s+(\w+)\s*\([^)]*\)\s*{', code)
        custom_functions = [f for f in custom_functions if f not in ['setup', 'loop']]
        
        if custom_functions:
            walkthrough += "### Custom Functions\n\n"
            for func in custom_functions:
                walkthrough += f"- `{func}()` - Helper function\n"
            walkthrough += "\n"
        
        return walkthrough
    
    def generate_troubleshooting(self, code: str, description: str) -> str:
        """Generate troubleshooting section."""
        
        troubleshooting = """# Troubleshooting Guide

## Compilation Issues

### Error: "Library not found"
**Symptoms:** `fatal error: XXX.h: No such file or directory`

**Solutions:**
1. Install missing library: `pio lib install "library-name"`
2. Check library spelling in #include
3. Verify platformio.ini lib_deps section
4. Clean and rebuild: `pio run --target clean`

### Error: "Undefined reference"
**Symptoms:** `undefined reference to 'functionName'`

**Solutions:**
1. Verify library is installed
2. Check function name spelling
3. Ensure all required #include statements present
4. Rebuild project completely

### Error: "Not enough memory"
**Symptoms:** Code too large for flash/RAM

**Solutions:**
1. Remove debug Serial.println() statements
2. Use F() macro for strings: `Serial.println(F("text"))`
3. Move large strings to PROGMEM
4. Reduce array sizes
5. Optimize loops and variables

## Upload Issues

### Error: "Failed to connect"
**Symptoms:** Cannot upload code to board

**Solutions:**
1. Check USB cable (use data cable, not charge-only)
2. Select correct COM port in PlatformIO
3. Install CH340/CP2102 USB drivers
4. Hold BOOT button while uploading
5. Try different USB port
6. Reset board before upload

### Error: "Timeout waiting for packet header"
**Solutions:**
1. Lower upload speed in platformio.ini:
   ```ini
   upload_speed = 115200
   ```
2. Press and hold BOOT button during upload
3. Reset board and retry immediately

## Runtime Issues

### Issue: Code doesn't execute
**Check:**
1. Serial monitor shows nothing → Check baud rate (115200)
2. LED doesn't blink → Check pin number
3. Sensor doesn't work → Check wiring
4. WiFi doesn't connect → Check SSID/password

**Debug steps:**
```cpp
void setup() {
    Serial.begin(115200);
    Serial.println("\\n\\n=== Starting ===");
    Serial.println("Testing...");
}
```

### Issue: Sensor reads incorrect values
**Common causes:**
1. **Wiring error** - Check VCC, GND, signal pins
2. **Power issues** - Use external power for multiple sensors
3. **I2C address conflict** - Run I2C scanner
4. **Timing issues** - Add delays after sensor init
5. **Pull-up resistors** - I2C needs 4.7kΩ resistors

**I2C Scanner Code:**
```cpp
#include <Wire.h>

void setup() {
    Wire.begin();
    Serial.begin(115200);
    Serial.println("I2C Scanner");
}

void loop() {
    for(byte i = 8; i < 120; i++) {
        Wire.beginTransmission(i);
        if(Wire.endTransmission() == 0) {
            Serial.print("Found: 0x");
            Serial.println(i, HEX);
        }
    }
    delay(5000);
}
```

### Issue: Board resets randomly
**Causes:**
1. Insufficient power (use 2A+ USB adapter)
2. Brown-out detection triggered
3. Watchdog timer reset
4. Code crashes (check array bounds)

**Solutions:**
1. Add `esp_task_wdt_reset()` in long loops
2. Use external 5V power supply
3. Add capacitors (100µF) on power rails
4. Check for infinite loops

## WiFi Issues

### Cannot connect to WiFi
**Debug code:**
```cpp
WiFi.begin("SSID", "password");
Serial.print("Connecting");
while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
}
Serial.println("\\nConnected!");
Serial.println(WiFi.localIP());
```

**Solutions:**
1. Check SSID and password spelling
2. Verify WiFi is 2.4GHz (not 5GHz)
3. Check signal strength
4. Disable MAC filtering on router
5. Try static IP instead of DHCP

### Random WiFi disconnects
**Solutions:**
1. Increase WiFi TX power:
   ```cpp
   WiFi.setTxPower(WIFI_POWER_19_5dBm);
   ```
2. Add reconnection logic:
   ```cpp
   if(WiFi.status() != WL_CONNECTED) {
       WiFi.reconnect();
   }
   ```
3. Reduce distance to router
4. Check for interference

## Safety Warnings

⚠️ **CRITICAL - READ BEFORE POWERING ON:**

1. **Voltage Limits**
   - ESP32 GPIO pins are 3.3V ONLY
   - Connecting 5V will **PERMANENTLY DAMAGE** the chip
   - Use level shifters for 5V devices

2. **Current Limits**
   - Maximum 12mA per GPIO pin
   - Maximum 40mA total for all pins
   - Use transistors/MOSFETs for high-current loads

3. **Power Supply**
   - USB provides max 500mA (often less)
   - Multiple sensors need external power
   - Use 5V/2A+ adapter for motors/servos

4. **Static Electricity**
   - Touch grounded metal before handling board
   - Use anti-static mat/wrist strap
   - Store in anti-static bag

5. **Short Circuits**
   - Double-check all connections
   - Keep metal objects away from powered board
   - Use insulated workspace

## Getting Help

If issues persist:

1. **Check Serial Monitor**
   - Baud rate: 115200
   - Look for error messages
   - Add debug print statements

2. **Search Online**
   - Arduino Forums
   - ESP32 subreddit
   - Stack Overflow

3. **Check Datasheets**
   - Sensor specifications
   - Pin configurations
   - Communication protocols

4. **Use Multimeter**
   - Verify power voltage (3.3V/5V)
   - Check continuity
   - Test for shorts

5. **Minimal Test Code**
   - Strip down to basics
   - Test one component at a time
   - Isolate the problem
"""
        
        return troubleshooting
    
    def generate_full_documentation(self, 
                                   code: str,
                                   description: str,
                                   libraries: List[str] = None) -> str:
        """Generate complete documentation."""
        
        if libraries is None:
            libraries = []
        
        # Extract libraries from code if not provided
        if not libraries:
            includes = re.findall(r'#include\s+[<"]([^>"]+)[>"]', code)
            libraries = includes
        
        doc = f"""# {description}

**Auto-generated Documentation**  
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## Table of Contents

1. [Overview](#overview)
2. [Hardware Setup](#hardware-setup-guide)
3. [Pin Configuration](#pin-configuration)
4. [Library Installation](#library-installation-guide)
5. [Code Walkthrough](#code-walkthrough)
6. [Troubleshooting](#troubleshooting-guide)
7. [Safety Information](#safety-warnings)

---

## Overview

This embedded systems project implements: **{description}**

### Quick Start
1. Install required libraries (see section below)
2. Wire components according to pin guide
3. Upload code to ESP32
4. Open Serial Monitor (115200 baud)
5. Monitor output and verify operation

---

"""
        
        # Add all sections
        doc += self.generate_hardware_guide(code, description) + "\n\n---\n\n"
        doc += self.generate_pin_guide(code) + "\n\n---\n\n"
        doc += self.generate_library_guide(code, libraries) + "\n\n---\n\n"
        doc += self.generate_code_walkthrough(code) + "\n\n---\n\n"
        doc += self.generate_troubleshooting(code, description) + "\n\n---\n\n"
        
        # Footer
        doc += """## Additional Resources

### Official Documentation
- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [Arduino Language Reference](https://www.arduino.cc/reference/en/)
- [PlatformIO Documentation](https://docs.platformio.org/)
- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)

### Community
- [ESP32 Forum](https://www.esp32.com/)
- [Arduino Forum](https://forum.arduino.cc/)
- [PlatformIO Community](https://community.platformio.org/)

### Tools
- [Serial Monitor](https://docs.platformio.org/en/latest/core/userguide/device/cmd_monitor.html)
- [I2C Scanner Tool](https://playground.arduino.cc/Main/I2cScanner/)
- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)

---

## License

This code and documentation are provided as-is for educational purposes.

**Support:** For issues or questions, consult the troubleshooting section above.

---

*Documentation auto-generated by MCP Documentation Generator (Phase 7)*
"""
        
        return doc

# ============================================================================
# TEST MODE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("📚 Documentation Generator Server - Test Mode")
    print("="*70 + "\n")
    
    # Sample ESP32 code for testing
    sample_code = """
#include <WiFi.h>
#include <DHT.h>
#include <Wire.h>
#include <PubSubClient.h>

#define DHT_PIN 23
#define DHT_TYPE DHT22
#define LED_PIN 2

const char* ssid = "YourWiFi";
const char* password = "YourPassword";

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    
    WiFi.begin(ssid, password);
    while(WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    dht.begin();
    client.setServer("mqtt.example.com", 1883);
}

void loop() {
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if(!isnan(temp) && !isnan(humidity)) {
        Serial.print("Temp: ");
        Serial.print(temp);
        Serial.print("°C, Humidity: ");
        Serial.print(humidity);
        Serial.println("%");
        
        digitalWrite(LED_PIN, HIGH);
        delay(100);
        digitalWrite(LED_PIN, LOW);
    }
    
    delay(2000);
}
"""
    
    server = DocsGeneratorServer()
    
    print("Test 1: Extract Hardware Info")
    print("-" * 70)
    hw_info = server.extract_hardware_info(sample_code)
    print(json.dumps(hw_info, indent=2))
    
    print("\n" + "="*70)
    print("Test 2: Generate Full Documentation")
    print("="*70 + "\n")
    
    description = "WiFi Temperature & Humidity Monitor with MQTT"
    libraries = ["adafruit/DHT-sensor-library", "knolleary/PubSubClient"]
    
    full_docs = server.generate_full_documentation(sample_code, description, libraries)
    
    # Save to file
    output_file = "test_documentation.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_docs)
    
    print(f"✓ Documentation generated ({len(full_docs)} chars)")
    print(f"✓ Saved to: {output_file}")
    print(f"\nPreview (first 500 chars):")
    print(full_docs[:500] + "...")
    
    print("\n" + "="*70)
    print("✅ All tests completed!")
    print("="*70)
