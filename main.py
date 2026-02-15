#!/usr/bin/env python3
# main.py - ESP32 Firmware AI Generator (SIMPLIFIED VERSION 3.2.0)
# Focus on code generation only - skip problematic library installation

import re
import os
import subprocess
import shutil
import json
import time
import configparser
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import sys

# Import MCP Client
from mcp_client import MCPClient
from mcp_servers.ollama_sampling_server import OllamaSamplingServer
from mcp_servers.docs_generator_server import DocsGeneratorServer

# Phase 8: Performance & Error Handling
from utils.response_cache import ResponseCache
from utils.error_handling import (
    CodeGenerationException, OllamaConnectionError, ValidationError,
    validate_description, validate_generated_code, retry_with_backoff, logger
)

from models import CodeGenerationResponse, CodeGenerationRequest

# ---- Windows UTF-8 fix (MANDATORY) ----
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---- Ensure Arduino CLI is on PATH (Windows) ----
if sys.platform.startswith("win"):
    arduino_cli_path = r'C:\Program Files\Arduino CLI'
    if os.path.exists(arduino_cli_path) and arduino_cli_path not in os.environ['PATH']:
        os.environ['PATH'] = arduino_cli_path + os.pathsep + os.environ['PATH']

load_dotenv()

app = FastAPI(
    title="ESP32 Firmware AI Generator",
    description="Code generation with smart library detection",
    version="3.2.0"
)

if os.path.exists("./static"):
    app.mount("/static", StaticFiles(directory="./static"), name="static")

# Initialize MCP Client
mcp_client = MCPClient()
print("✓ MCP Client initialized")

# Initialize Ollama Sampling Server (Phase 6)
ollama_sampler = OllamaSamplingServer()
print("✓ Ollama Sampling Server initialized")

# Initialize Documentation Generator (Phase 7)
docs_generator = DocsGeneratorServer()
print("✓ Documentation Generator initialized")

# Initialize Response Cache (Phase 8)
response_cache = ResponseCache(ttl_minutes=30, max_size=100)
print("✓ Response Cache initialized (30min TTL, max 100 entries)")
# --- NEW: Evaluation Metrics ---
EVAL_METRICS = {
    "total_requests": 0,
    "compile_attempts": 0,
    "compile_successes": 0,
    "quality_score_total": 0.0
}


try:
    import ollama
    USING_OLLAMA = True
except ImportError:
    USING_OLLAMA = False

USING_OPENAI = False
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    try:
        from openai import OpenAI
        USING_OPENAI = True
    except ImportError:
        USING_OPENAI = False

PLATFORMIO_PROJECT_PATH = os.getenv("PLATFORMIO_PROJECT_PATH", "./esp32_project")
PLATFORMIO_SRC_PATH = os.path.join(PLATFORMIO_PROJECT_PATH, "src")
PLATFORMIO_INI_PATH = os.path.join(PLATFORMIO_PROJECT_PATH, "platformio.ini")
DOCS_PATH = os.path.join(PLATFORMIO_PROJECT_PATH, "docs")

ARDUINO_BUILD_PATH = os.getenv("ARDUINO_BUILD_PATH", "./arduino_builds")

os.makedirs(PLATFORMIO_SRC_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)
os.makedirs(ARDUINO_BUILD_PATH, exist_ok=True)

LIBRARY_MAPPING = {
    "DHT.h": "adafruit/DHT-sensor-library",
    "Adafruit_Sensor.h": "adafruit/Adafruit-Unified-Sensor",
    "OneWire.h": "paulstoffregen/OneWire",
    "DallasTemperature.h": "milesburton/DallasTemperature",
    "BMP085.h": "adafruit/Adafruit-BMP085-Library",
    "MPU6050.h": "jrowberg/MPU6050",
    "BMP280.h": "adafruit/Adafruit-BMP280-Library",
    "INA219.h": "adafruit/Adafruit-INA219",
    "ADXL345.h": "adafruit/Adafruit-ADXL345",
    "HTU21D.h": "sparkfun/SparkFun-HTU21D-Humidity-and-Temperature-Sensor",
    "BH1750.h": "claws/BH1750",
    "TSL2561.h": "adafruit/Adafruit-TSL2561",
    "VL53L0X.h": "pololu/VL53L0X",
    "MLX90614.h": "adafruit/Adafruit-MLX90614-Library",
    "LiquidCrystal_I2C.h": "mathertel/LiquidCrystal_I2C",
    "SSD1306.h": "adafruit/Adafruit-SSD1306",
    "TM1637.h": "avishorp/TM1637",
    "Adafruit_ST7735.h": "adafruit/Adafruit-ST7735-Library",
    "Adafruit_ILI9341.h": "adafruit/Adafruit-ILI9341",
    "GxEPD.h": "ZinggJM/GxEPD",
    "MAX7219.h": "sparkfun/SparkFun-LED-Array-8x8",
    "ws2812b.h": "kitesurfer1404/WS2812FX",
    "NeoPixel.h": "adafruit/Adafruit-NeoPixel",
    "PubSubClient.h": "knolleary/PubSubClient",
    "AsyncTCP.h": "me-no-dev/AsyncTCP",
    "ESPAsyncWebServer.h": "me-no-dev/ESPAsyncWebServer",
    "WiFiManager.h": "tzapu/WiFiManager",
    "BluetoothSerial.h": "builtin",
    "BLEDevice.h": "builtin",
    "LoRa.h": "sandeepmistry/arduino-LoRa",
    "RH_RF95.h": "sparkfun/RadioHead",
    "ArduinoJson.h": "bblanchon/ArduinoJson",
    "LittleFS.h": "builtin",
    "SPIFFS.h": "builtin",
    "SD.h": "builtin",
    "FS.h": "builtin",
    "Servo.h": "builtin",
    "ESP32Servo.h": "madhephaestus/ESP32Servo",
    "AccelStepper.h": "mike-matera/AccelStepper",
    "Motor.h": "builtin",
    "NTPClient.h": "taranais/NTPClient",
    "TimeLib.h": "PaulStoffregen/Time",
    "CAN.h": "sandeepmistry/CAN",
    "SoftwareSerial.h": "builtin",
    "Arduino.h": "builtin",
    "Wire.h": "builtin",
    "SPI.h": "builtin",
    "WiFi.h": "builtin",
    "WebServer.h": "builtin",
    "HTTPClient.h": "builtin",
    "EEPROM.h": "builtin",
    "Serial.h": "builtin",
    "pins_arduino.h": "builtin",
    "esp_wifi.h": "builtin",
    "esp_now.h": "builtin",
    "nvs_flash.h": "builtin",
    "driver/gpio.h": "builtin",
    "driver/adc.h": "builtin",
    "driver/uart.h": "builtin",
    "driver/ledc.h": "builtin",
}

if USING_OPENAI:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found")
    openai_client = OpenAI(api_key=openai_api_key)
    LLM_MODEL = "gpt-4o-mini"
    print(f"✓ OpenAI initialized: {LLM_MODEL}")
elif USING_OLLAMA:
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        ollama_client = ollama.Client(host=ollama_host)
        LLM_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")
        print(f"✓ Ollama initialized: {LLM_MODEL}")
    except Exception as e:
        raise ConnectionError(f"Cannot connect to Ollama at {ollama_host}: {e}")
else:
    raise ImportError("Neither OpenAI nor Ollama are available")

def extract_includes_from_code(code: str) -> List[str]:
    """Extract all #include statements from generated code."""
    includes = []
    include_pattern = r'#include\s+[<"]([a-zA-Z0-9_./\-]+\.h)[>"]'
    matches = re.findall(include_pattern, code, re.IGNORECASE)
    
    for match in matches:
        header = match.strip()
        if header and header not in includes:
            includes.append(header)
    
    return includes

def detect_required_libraries(code: str) -> List[tuple]:
    """SMART Library Detection - Extract #include from code."""
    required_libs = []
    
    print("\n" + "="*70)
    print("SMART LIBRARY DETECTION")
    print("="*70)
    
    includes = extract_includes_from_code(code)
    print(f"\n✓ Found {len(includes)} #include statements:")
    for inc in includes:
        print(f"  - {inc}")
    
    if not includes:
        print("\n✓ No external libraries needed")
        return []
    
    print(f"\n--- Library Mapping ---")
    for header in includes:
        if header in LIBRARY_MAPPING:
            lib_name = LIBRARY_MAPPING[header]
            if lib_name == "builtin":
                print(f"  {header}: BUILTIN (Arduino framework) - skip")
                continue
            
            required_libs.append((header, lib_name))
            print(f"  {header}: {lib_name}")
        else:
            print(f"  {header}: NOT MAPPED (custom library)")
    
    print(f"\n✓ Total libraries needed: {len(required_libs)}")
    print("="*70 + "\n")
    
    return required_libs

def generate_installation_guide(libraries: List[tuple]) -> str:
    """Generate manual installation instructions for libraries."""
    if not libraries:
        return ""
    
    guide = """
📚 MANUAL LIBRARY INSTALLATION GUIDE
=====================================

Your code needs the following external libraries.
Install them using the PlatformIO IDE or command line.

METHOD 1: Using PlatformIO CLI (Command Line)
----------------------------------------------
"""
    
    for header, lib_name in libraries:
        guide += f"\n➤ {header}\n"
        guide += f"  Command: pio lib install \"{lib_name}\"\n"
        guide += f"  Or:      pio lib install {lib_name.split('/')[-1]}\n"
    
    guide += """

METHOD 2: Using PlatformIO IDE
-------------------------------
1. Open Home → Libraries
2. Search for library by name
3. Click "Install"
4. Restart Reload

METHOD 3: Manual platformio.ini
-------------------------------
Add to D:\\MCP\\esp32_project\\platformio.ini:

[env:esp32dev]
lib_deps =
"""
    
    for header, lib_name in libraries:
        guide += f"    {lib_name}\n"
    
    guide += """

Then PlatformIO will auto-install when you compile.

⚠️ NOTE:
If you get "UnknownPackageError" on Windows, use the simple name:
  pio lib install DHT-sensor-library
  (instead of: pio lib install adafruit/DHT-sensor-library)
"""
    
    return guide

def make_unique_filename(description: str, ext: str = ".cpp") -> str:
    """Generate unique filename - remove ALL special characters."""
    cleaned = description.strip().lower()
    cleaned = re.sub(r"[^a-z0-9\s_\-]", "", cleaned)
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("_")
    
    if not cleaned or cleaned == "":
        cleaned = "generated"
    
    if len(cleaned) > 35:
        cleaned = cleaned[:35]
    
    timestamp = int(time.time())
    return f"{cleaned}_{timestamp}{ext}"

def save_code_to_file(code: str, description: str) -> str:
    """Save generated code to file."""
    filename = make_unique_filename(description, ".cpp")
    filepath = os.path.join(PLATFORMIO_SRC_PATH, filename)
    
    with open(filepath, "w") as f:
        f.write(code)
    
    return filepath

def clean_code_output(raw_response: str) -> str:
    """Extract code from LLM response."""
    try:
        blocks = re.findall(r"```(?:cpp|c\+\+|c)?\s*([\s\S]*?)```", raw_response, re.IGNORECASE)
        if blocks:
            code = max(blocks, key=lambda b: len(b.strip()))
            return code.strip()
        return raw_response.strip()
    except Exception:
        return raw_response.strip()

def compile_code() -> dict:
    """Deprecated PlatformIO stub. Use Arduino CLI helpers instead."""
    return {"success": False, "output": "PlatformIO compile not used. Configure Arduino CLI.", "returncode": -1}


# --- Arduino CLI helpers (preferred) ---
ARDUINO_BOARD_MAP = {
    "esp32": "esp32:esp32:esp32",
    "uno": "arduino:avr:uno",
    "nano": "arduino:avr:nano",
    "default": "esp32:esp32:esp32"
}

def check_arduino_cli() -> str:
    """Return path to arduino-cli or empty string."""
    return shutil.which("arduino-cli") or ""

def ensure_core_installed(fqbn: str) -> dict:
    """Try to install/update core required by FQBN. Returns dict with output."""
    arduino = check_arduino_cli()
    if not arduino:
        return {"success": False, "output": "arduino-cli not found"}

    parts = fqbn.split(":")
    if len(parts) < 2:
        return {"success": False, "output": f"Invalid FQBN: {fqbn}"}

    platform = ":".join(parts[:2])
    try:
        cmd_index = [arduino, "core", "update-index"]
        idx = subprocess.run(cmd_index, capture_output=True, text=True, timeout=120)

        cmd_install = [arduino, "core", "install", platform]
        inst = subprocess.run(cmd_install, capture_output=True, text=True, timeout=300)

        return {"success": inst.returncode == 0, "output": idx.stdout + idx.stderr + inst.stdout + inst.stderr, "returncode": inst.returncode}
    except Exception as e:
        return {"success": False, "output": str(e)}

def save_sketch_as_ino(code: str, description: str) -> tuple:
    """Create a sketch folder and save code as <sketch_name>.ino. Returns (sketch_dir, sketch_file)."""
    # Reuse make_unique_filename to create safe name but without extension
    name = make_unique_filename(description, ext="")
    sketch_dir = os.path.join(ARDUINO_BUILD_PATH, name)
    os.makedirs(sketch_dir, exist_ok=True)
    sketch_file = os.path.join(sketch_dir, f"{name}.ino")
    with open(sketch_file, "w", encoding="utf-8") as f:
        f.write(code)
    return sketch_dir, sketch_file

def install_libraries_arduino(detected_libraries: List[tuple]) -> dict:
    """Install libraries via arduino-cli lib install. Returns aggregated output."""
    arduino = check_arduino_cli()
    if not arduino:
        return {"success": False, "output": "arduino-cli not found"}

    outputs = []
    for header, lib_name in detected_libraries:
        # prefer simple name if given like adafruit/DHT-sensor-library -> DHT-sensor-library
        lib_arg = lib_name.split("/")[-1]
        cmd = [arduino, "lib", "install", lib_arg]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            outputs.append("\n".join([" ".join(cmd), r.stdout, r.stderr]))
        except Exception as e:
            outputs.append(f"Error running {' '.join(cmd)}: {e}")

    return {"success": True, "output": "\n".join(outputs)}

def arduino_compile_sketch(sketch_dir: str, fqbn: str, detected_libraries: Optional[List[tuple]] = None) -> dict:
    """Compile a sketch using arduino-cli. Returns dict with detailed diagnostics."""
    arduino = check_arduino_cli()
    if not arduino:
        return {"success": False, "output": "❌ arduino-cli not found in PATH", "returncode": -1, "tool_path": None}

    # Prepare environment and file list
    cwd = os.path.abspath(sketch_dir)
    file_list = []
    for root, dirs, files in os.walk(cwd):
        for f in files:
            file_list.append(os.path.relpath(os.path.join(root, f), cwd))

    env = os.environ.copy()

    # Ensure core is installed (best-effort)
    core_info = ensure_core_installed(fqbn)

    # Install libraries if requested
    libs_info = None
    if detected_libraries:
        libs_info = install_libraries_arduino(detected_libraries)

    cmd = [arduino, "compile", "--fqbn", fqbn, ".", "--build-path", os.path.join(cwd, "build"), "--verbose"]

    try:
        result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
        combined_output = []
        combined_output.append(f"Command: {' '.join(cmd)}")
        combined_output.append(f"Tool Path: {arduino}")
        combined_output.append(f"CWD: {cwd}")
        combined_output.append(f"PATH: {env.get('PATH')}")
        combined_output.append("\n--- FILES ---\n" + "\n".join(file_list))
        combined_output.append("\n--- CORE INFO ---\n" + str(core_info.get('output', '')))
        if libs_info:
            combined_output.append("\n--- LIBS INFO ---\n" + str(libs_info.get('output', '')))
        combined_output.append("\n--- COMPILE OUTPUT ---\n" + result.stdout + result.stderr)

        # Attempt to locate compiled binary
        build_dir = os.path.join(cwd, "build")
        binary_path = None
        if os.path.exists(build_dir):
            for root, dirs, files in os.walk(build_dir):
                for f in files:
                    if f.endswith(".bin") or f.endswith(".hex") or f.endswith(".elf"):
                        binary_path = os.path.join(root, f)
                        break
                if binary_path:
                    break

        return {
            "success": result.returncode == 0,
            "output": "\n".join(combined_output),
            "returncode": result.returncode,
            "tool_path": arduino,
            "cwd": cwd,
            "file_list": file_list,
            "binary_path": binary_path
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "⏱ Compilation timed out", "returncode": -1, "tool_path": arduino, "cwd": cwd, "file_list": file_list}
    except Exception as e:
        return {"success": False, "output": f"❌ Error: {str(e)}", "returncode": -1, "tool_path": arduino, "cwd": cwd, "file_list": file_list}


def preflight_check_arduino() -> dict:
    """Check Arduino CLI availability and core installation status. Returns diagnostic info."""
    arduino = check_arduino_cli()
    result = {
        "arduino_cli_found": bool(arduino),
        "arduino_cli_path": arduino,
        "cores_installed": {},
        "install_commands": [],
        "status_message": ""
    }

    if not arduino:
        result["status_message"] = (
            "❌ arduino-cli not found on PATH.\n\n"
            "INSTALLATION STEPS (Windows):\n"
            "1. Using Chocolatey: choco install arduino-cli\n"
            "2. Using Scoop: scoop install arduino-cli\n"
            "3. Manual: Download from https://github.com/arduino/arduino-cli/releases\n"
            "   Extract and add to PATH.\n\n"
            "After installation, run:\n"
            "  arduino-cli core update-index\n"
            "  arduino-cli core install esp32:esp32\n"
            "  arduino-cli core install arduino:avr"
        )
        return result

    result["status_message"] = "✓ arduino-cli found"

    # Check for required cores
    for platform, desc in [("esp32:esp32", "ESP32"), ("arduino:avr", "Arduino AVR")]:
        try:
            cmd = [arduino, "core", "list"]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            is_installed = platform in r.stdout
            result["cores_installed"][platform] = is_installed
            if not is_installed:
                result["install_commands"].append(f"arduino-cli core install {platform}")
        except Exception as e:
            result["cores_installed"][platform] = False
            result["install_commands"].append(f"arduino-cli core install {platform} (check failed: {str(e)})")

    if result["install_commands"]:
        result["status_message"] += f"\n⚠️  Some cores need installation:\n" + "\n".join(result["install_commands"])

    return result


def parse_compilation_errors(output: str) -> Dict:
    """Parse compilation errors."""
    errors_dict = {
        "syntax_errors": [],
        "missing_headers": [],
        "undefined_references": [],
        "type_errors": [],
        "ledc_api_errors": [],
        "other_errors": []
    }
    
    for line in output.split("\n"):
        if "error:" not in line.lower():
            continue
        
        line_clean = line.strip()
        if not line_clean:
            continue
        
        # Check for LEDC API errors (old API incompatible with v3.x)
        if ("ledcAttachPin" in line or "GPIO_NUM_" in line) and "not declared" in line.lower():
            errors_dict["ledc_api_errors"].append(line_clean)
        elif "fatal error:" in line.lower() and ".h:" in line:
            errors_dict["missing_headers"].append(line_clean)
        elif "undefined reference" in line.lower():
            errors_dict["undefined_references"].append(line_clean)
        elif "error:" in line.lower() and ("expected" in line or "undeclared" in line):
            errors_dict["syntax_errors"].append(line_clean)
        elif "error:" in line.lower() and ("type" in line or "cannot" in line):
            errors_dict["type_errors"].append(line_clean)
        else:
            errors_dict["other_errors"].append(line_clean)
    
    return errors_dict

def generate_troubleshooting_suggestions(error_dict: Dict) -> List[str]:
    """Generate troubleshooting suggestions."""
    suggestions = []
    
    if error_dict["missing_headers"]:
        suggestions.append("📦 Missing libraries - see installation guide above")
    if error_dict["syntax_errors"]:
        suggestions.append("🔧 Syntax errors detected")
    if error_dict["undefined_references"]:
        suggestions.append("🔗 Undefined references - check library installation")
    if error_dict["type_errors"]:
        suggestions.append("⚠ Type errors detected")
    if error_dict.get("ledc_api_errors"):
        suggestions.append("⚙ LEDC API error - using deprecated functions. Attempting auto-repair...")
    if error_dict["other_errors"]:
        suggestions.append("❓ Other errors detected. Check compilation output.")
    
    if not any([error_dict[k] for k in error_dict if k != "ledc_api_errors"]):
        suggestions.append("✓ No compilation errors detected.")
    
    return suggestions

def repair_ledc_api_code(code: str, error_output: str) -> str:
    """Auto-repair LEDC API errors (ledcAttachPin -> ledcAttach migration)."""
    
    # Replace deprecated ledcAttachPin with modern API
    repaired = code
    
    # Pattern 1: Replace ledcAttachPin(pin, channel) with digitalWrite-based approach
    # If simple blink, use digitalWrite instead
    if "ledcAttachPin" in repaired and "digitalWrite" not in repaired:
        print("🔧 Auto-repairing LEDC API: Converting to modern API or digitalWrite...")
        
        # Remove ledcSetup and ledcAttachPin calls if it's a simple blink
        if "void loop()" in repaired and "delay" in repaired:
            # Simple blink pattern detected - use digitalWrite
            repaired = repaired.replace("ledcSetup(", "// ledcSetup(")
            repaired = repaired.replace("ledcAttachPin(", "// ledcAttachPin(")
            repaired = repaired.replace("ledcWrite(", "digitalWrite(")
            # Add pinMode if not present
            if "pinMode(" not in repaired:
                setup_idx = repaired.find("void setup()")
                if setup_idx != -1:
                    setup_end = repaired.find("Serial.begin", setup_idx)
                    if setup_end != -1:
                        # Insert pinMode after Serial.begin
                        insert_idx = repaired.find(";", setup_end) + 1
                        repaired = repaired[:insert_idx] + "\n  pinMode(14, OUTPUT);  // Fixed: added pinMode" + repaired[insert_idx:]
            print("  ✓ Converted to digitalWrite (simple blink)")
    
    # Replace GPIO_NUM_14 with plain 14
    repaired = repaired.replace("GPIO_NUM_14", "14")
    repaired = repaired.replace("GPIO_NUM_", "")
    
    return repaired


# --- Library detection and automatic install helpers ---
HEADER_TO_LIB = {
    "DHT.h": "adafruit/DHT-sensor-library",
    "Adafruit_SSD1306.h": "adafruit/Adafruit_SSD1306",
    "Adafruit_GFX.h": "adafruit/Adafruit-GFX-Library",
    "MPU6050.h": "ElectronicWings/MPU6050",
    "MAX30102.h": "SparkFun/MAX30105_Sensor",
    "MAX30105.h": "SparkFun/MAX30105_Sensor",
    "BH1750.h": "adafruit/Adafruit_BH1750",
    "DHT_U.h": "adafruit/DHT-sensor-library",
    "Adafruit_BME280.h": "adafruit/Adafruit_BME280_Library",
    "SSD1306.h": "adafruit/Adafruit_SSD1306",
    # Add more mappings as needed
}
# Merge with existing mapping to reuse the comprehensive table
try:
    HEADER_TO_LIB.update(LIBRARY_MAPPING)
except Exception:
    pass

LIB_CACHE_FILE = os.path.join(ARDUINO_BUILD_PATH, "arduino_lib_cache.json")

def _load_lib_cache() -> dict:
    try:
        if os.path.exists(LIB_CACHE_FILE):
            with open(LIB_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {"installed": []}

def _save_lib_cache(cache: dict):
    try:
        os.makedirs(os.path.dirname(LIB_CACHE_FILE), exist_ok=True)
        with open(LIB_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except Exception:
        pass

# NOTE: `detect_required_libraries` is defined earlier (uses LIBRARY_MAPPING).
# The earlier definition is preferred; keep helper functions below.

def _arduino_cli_search(lib_query: str) -> list:
    """Search arduino-cli library index and return parsed JSON results (if any)."""
    arduino = check_arduino_cli()
    if not arduino:
        return []
    try:
        cmd = [arduino, "lib", "search", lib_query, "--format", "json"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout:
            try:
                data = json.loads(r.stdout)
                if isinstance(data, list):
                    return data
            except Exception:
                # Non-JSON fallback: ignore
                return []
    except Exception:
        pass
    return []

def install_libraries_with_arduino_cli(detected_libraries: List[tuple]) -> dict:
    """Attempt to install each detected library using arduino-cli. Returns a dependency report."""
    report = {
        "detected_includes": [h for h, _ in detected_libraries],
        "libraries_attempted": [],
        "installed": [],
        "failed": []
    }

    cache = _load_lib_cache()
    installed_cache = set(cache.get("installed", []))

    arduino = check_arduino_cli()
    if not arduino:
        for h, mapped in detected_libraries:
            report["failed"].append({"name": mapped or h, "reason": "arduino-cli not found", "suggestion": "Install arduino-cli"})
        return report

    for header, mapped in detected_libraries:
        candidate = mapped or header.replace('.h', '')
        report["libraries_attempted"].append(candidate)

        if candidate in installed_cache:
            report["installed"].append(candidate)
            continue

        # Try to search for the mapped library name first
        search_results = _arduino_cli_search(candidate)
        chosen = None
        if search_results:
            # Prefer the first result's name if available
            first = search_results[0]
            chosen = first.get("name") or first.get("ID") or candidate
        else:
            chosen = candidate

        # Attempt install
        try:
            cmd = [arduino, "lib", "install", chosen]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            out = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0:
                report["installed"].append(chosen)
                installed_cache.add(candidate)
            else:
                report["failed"].append({"name": candidate, "reason": out.strip() or f"Return code {r.returncode}", "suggestion": "Try manual install or check library name"})
        except Exception as e:
            report["failed"].append({"name": candidate, "reason": str(e), "suggestion": "Exception during subprocess"})

    # Save cache
    cache["installed"] = list(installed_cache)
    _save_lib_cache(cache)

    return report

def _extract_missing_headers_from_output(output: str) -> List[str]:
    """Extract header filenames reported as missing in compile output."""
    missing = []
    for line in output.splitlines():
        if "fatal error:" in line.lower() and ": No such file or directory" in line:
            m = re.search(r"fatal error:\s*([^:]+\.h)", line, re.IGNORECASE)
            if m:
                header = os.path.basename(m.group(1).strip())
                missing.append(header)
    # dedupe
    return list(dict.fromkeys(missing))

def compile_with_retries(sketch_dir: str, fqbn: str, detected_libraries: List[tuple], max_retries: int = 2, initial_dependency_report: dict = None) -> dict:
    """Compile and auto-install missing libraries up to `max_retries` times.

    Returns final compile_result and attaches a dependency_report under key 'dependency_report'.
    """
    dependency_report = initial_dependency_report or {"detected_includes": [h for h, _ in detected_libraries], "libraries_attempted": [], "installed": [], "failed": []}

    attempt = 0
    last_result = None
    while attempt <= max_retries:
        last_result = arduino_compile_sketch(sketch_dir, fqbn, detected_libraries)
        if last_result.get("success"):
            last_result["dependency_report"] = dependency_report
            return last_result

        output = last_result.get("output", "") or ""
        missing = _extract_missing_headers_from_output(output)
        if not missing:
            # No missing header detected - stop retrying
            last_result["dependency_report"] = dependency_report
            return last_result

        # Map missing headers to libraries
        to_install = []
        for h in missing:
            mapped = HEADER_TO_LIB.get(h)
            to_install.append((h, mapped))

        print(f"🔁 Detected missing headers: {missing}. Attempting to install corresponding libraries...")
        report = install_libraries_with_arduino_cli(to_install)
        # Merge reports
        dependency_report["libraries_attempted"].extend(report.get("libraries_attempted", []))
        dependency_report["installed"].extend(report.get("installed", []))
        dependency_report["failed"].extend(report.get("failed", []))

        # Retry
        attempt += 1
        print(f"  → Retry #{attempt} after installing libraries")

    last_result["dependency_report"] = dependency_report
    return last_result

def ollama_chat_with_fallback(messages: List[Dict[str, str]]) -> Dict:
    """Call Ollama and retry once on the alternate local port."""
    global ollama_client, ollama_host
    try:
        return ollama_client.chat(
            model=LLM_MODEL,
            messages=messages,
            stream=False
        )
    except Exception as first_error:
        current_host = globals().get("ollama_host", os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        fallback_host = "http://localhost:11435" if "11434" in current_host else "http://localhost:11434"
        try:
            alt_client = ollama.Client(host=fallback_host)
            response = alt_client.chat(
                model=LLM_MODEL,
                messages=messages,
                stream=False
            )
            ollama_client = alt_client
            ollama_host = fallback_host
            print(f"Switched Ollama host to {fallback_host}")
            return response
        except Exception:
            raise first_error


def generate_code_with_llm(description: str, context: Optional[str] = None) -> str:
    """Generate ESP32 code using LLM."""
    
    system_prompt = """You are an expert ESP32 firmware developer using ESP32 Arduino core v3.x.
    
REQUIREMENTS:
1. Generate ONLY complete Arduino sketches
2. Use void setup() and void loop()
3. Do NOT include fake libraries
4. Use Arduino standard functions only
5. For simple blink/digitalWrite: Use digitalWrite directly, NO PWM
6. For PWM frequency/brightness control ONLY:
   - Use: pinMode(pin, OUTPUT); digitalWrite(pin, value);
   - OR use modern LEDC: ledcAttach(pin, freq, bits) then ledcWrite(pin, value)
   - NEVER use deprecated ledcAttachPin() or GPIO_NUM_* constants
7. Use plain pin numbers (14, 2, etc), NOT GPIO_NUM_14
8. Include Serial.begin(115200) if needed
9. Return ONLY code in ```cpp``` blocks
10. Keep code simple - prefer digitalWrite over complex PWM setups"""
    
    user_message = f"Generate ESP32 Arduino code for: {description}"
    if context:
        user_message += f"\n\nContext: {context}"
    
    try:
        if USING_OPENAI:
            response = openai_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.6,
                max_tokens=2048
            )
            return response.choices[0].message.content
        
        elif USING_OLLAMA:
            response = ollama_chat_with_fallback([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            return response["message"]["content"]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

def generate_documentation_with_llm(code: str, description: str) -> str:
    """Generate markdown documentation."""
    
    doc_prompt = f"""Generate markdown documentation for this ESP32 code.

Description: {description}

Code:
{code}

Include:
1. Project Overview
2. Hardware Requirements
3. Libraries Used
4. How It Works
5. Pin Configuration
6. Troubleshooting

Return ONLY markdown, no code blocks."""
    
    try:
        if USING_OPENAI:
            response = openai_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a technical writer."},
                    {"role": "user", "content": doc_prompt}
                ],
                temperature=0.5,
                max_tokens=2048
            )
            return response.choices[0].message.content
        
        elif USING_OLLAMA:
            response = ollama_chat_with_fallback([
                {"role": "system", "content": "You are a technical writer."},
                {"role": "user", "content": doc_prompt}
            ])
            return response["message"]["content"]
    
    except Exception as e:
        print(f"⚠ Documentation error: {str(e)}")
        return None

def save_documentation(documentation: str, code_filename: str) -> str:
    """Save documentation to file."""
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)
    
    base_filename = os.path.splitext(os.path.basename(code_filename))[0]
    doc_filename = f"{base_filename}_README.md"
    doc_path = os.path.join(DOCS_PATH, doc_filename)
    
    try:
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(documentation)
        print(f"✓ Documentation saved")
        return doc_path
    except Exception as e:
        print(f"⚠ Documentation save error: {str(e)}")
        return None

def cleanup_old_files(max_files: int = 3):
    """Remove old generated files."""
    try:
        if not os.path.exists(PLATFORMIO_SRC_PATH):
            return
        
        files = sorted(
            [f for f in os.listdir(PLATFORMIO_SRC_PATH) if f.endswith(".cpp")],
            key=lambda x: os.path.getmtime(os.path.join(PLATFORMIO_SRC_PATH, x)),
            reverse=True
        )
        
        if len(files) > max_files:
            for old_file in files[max_files:]:
                try:
                    os.remove(os.path.join(PLATFORMIO_SRC_PATH, old_file))
                except Exception:
                    pass
    except Exception:
        pass

@app.get("/")
async def root():
    """Serve web UI."""
    return FileResponse("./static/index.html", media_type="text/html")

@app.get("/health")
async def health_check():
    """Health check endpoint with Phase 8 enhancements."""
    pio_installed = os.system("pio --version > /dev/null 2>&1") == 0
    arduino_cli_path = check_arduino_cli()
    
    # Get cache statistics
    cache_stats = response_cache.get_stats()
    
    return {
        "status": "healthy",
        "backend": "Ollama" if USING_OLLAMA else "OpenAI" if USING_OPENAI else "None",
        "model": LLM_MODEL,
        "platformio_installed": pio_installed,
        "arduino_cli_installed": bool(arduino_cli_path),
        "arduino_cli_path": arduino_cli_path,
        "version": "3.2.0-phase8",
        "cache": cache_stats,
        "features": {
            "mcp_client": True,
            "ollama_sampling": True,
            "docs_generator": True,
            "response_cache": True,
            "error_handling": True
        }
    }

@app.get("/products/")
async def get_products():
    """Placeholder products endpoint for frontend compatibility."""
    return []

@app.post("/api/clarifying-questions")
async def get_clarifying_questions(request: CodeGenerationRequest):
    """Get clarifying questions for better code generation (Phase 6)."""
    try:
        questions = ollama_sampler.generate_clarifying_questions(
            request.description,
            num_questions=3
        )
        return {
            "initial_prompt": request.description,
            "clarifying_questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@app.post("/api/refine-and-generate")
async def refine_and_generate(
    initial_prompt: str,
    questions_answers: Dict[str, str],
    compile: bool = True,
    generate_docs: bool = True
):
    """Refine requirements and generate improved code (Phase 6)."""
    try:
        # Refine requirements
        print(f"\n{'='*70}")
        print(f"🔮 Refining requirements for: {initial_prompt}")
        print(f"{'='*70}")
        
        refined = ollama_sampler.refine_requirements(
            initial_prompt,
            questions_answers
        )
        print(f"✓ Requirements refined")
        
        # Generate improved prompt
        improved_prompt = ollama_sampler.generate_improved_prompt(
            initial_prompt,
            refined
        )
        print(f"✓ Improved prompt generated")
        
        # Use existing code generation with improved context
        request = CodeGenerationRequest(
            description=initial_prompt,
            context=improved_prompt,
            compile=compile,
            generate_docs=generate_docs
        )
        
        return await generate_code(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")

@app.post("/api/generate-code", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate ESP32 firmware code with Phase 8 optimizations."""
    
    # Phase 8: Input validation
    try:
        validate_description(request.description)
    except ValidationError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    # Phase 8: Check cache first
    cache_key = response_cache.get_cache_key(
        description=request.description,
        context=request.context or "",
        compile=request.compile,
        generate_docs=request.generate_docs
    )
    
    cached_response = response_cache.get(cache_key)
    if cached_response:
        logger.info("Using cached response")
        print("\n" + "="*70)
        print("⚡ Cache Hit! Returning cached response")
        print("="*70)
        # Return cached response (would need to deserialize)
        # For now, continue with generation
    
    cleanup_old_files(max_files=2)
    
    print(f"\n{'='*70}")
    print(f"📝 Generating: {request.description}")
    print(f"{'='*70}")
    
    # --- NEW: Evaluation Metrics ---
    generation_time = 0.0
    compilation_time = 0.0
    lines_of_code = 0
    compilation_success_rate = None
    average_quality_score = None
    memory_efficiency_score = None
    evaluation_summary = None
    mermaid_code = None
    mermaid_url = None

    # Phase 8: Code generation with error handling
    try:
        generation_start = time.time()
        logger.info(f"Starting code generation: {request.description[:50]}...")
        generated = generate_code_with_llm(request.description, request.context)
        code_only = clean_code_output(generated if isinstance(generated, str) else str(generated or ""))

        # Retry once if model returns empty/non-code output.
        if not code_only.strip():
            logger.warning("Primary LLM response was empty. Retrying with strict code-only context.")
            retry_context = (request.context + "\n\n" if request.context else "") + (
                "Return only Arduino C++ code with void setup() and void loop(). "
                "Do not include explanations."
            )
            generated_retry = generate_code_with_llm(request.description, retry_context)
            code_only = clean_code_output(
                generated_retry if isinstance(generated_retry, str) else str(generated_retry or "")
            )

        generation_time = time.time() - generation_start
        lines_of_code = len([line for line in code_only.splitlines() if line.strip()])
        
        # Phase 8: Validate generated code
        validate_generated_code(code_only)
        logger.info("Code generation successful")
        
    except ValidationError as e:
        logger.error(f"Generated code validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Invalid code generated: {str(e)}")
    except OllamaConnectionError as e:
        logger.error(f"Ollama connection error: {e}")
        raise HTTPException(status_code=503, detail="Code generation service unavailable")
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")
    
    filepath = save_code_to_file(code_only, request.description)
    print(f"✓ Code saved: {filepath}")
    
    compilation_status = None
    compilation_output = None
    detected_libraries = None
    error_summary = None
    troubleshooting_suggestions = []
    compilation_error_summary = None
    compiled_binary_path = None
    documentation = None
    installation_guide = None
    dependency_report = None
    compiler_used = None
    compile_success = None
    
    # DETECT LIBRARIES (NO INSTALLATION)
    print(f"\n>>> Smart library detection...")
    detected_libraries = detect_required_libraries(code_only)
    
    if detected_libraries:
        installation_guide = generate_installation_guide(detected_libraries)
        print(f"\n📚 Generated installation guide for {len(detected_libraries)} libraries")
    
    # MCP CLIENT ANALYSIS
    print(f"\n>>> Querying MCP servers for analysis...")
    
    # 1. Hardware specs (WRAPPED with fallback)
    try:
        hardware_specs = mcp_client.get_board_specs("esp32dev")
        print(f"✓ Got hardware specs: {hardware_specs['name']}")
    except Exception as e:
        logger.warning(f"Hardware specs query failed: {e}. Using fallback.")
        hardware_specs = {
            "name": "ESP32 DevKit V1",
            "flash_mb": 4,
            "ram_kb": 520,
            "gpio_pins": 40,
            "adc_channels": 18,
            "uart_ports": 3,
            "i2c_ports": 2,
            "spi_ports": 3,
            "pwm_channels": 16
        }
    
    # 2. Library analysis (WRAPPED with fallback)
    try:
        library_analysis = mcp_client.analyze_libraries(code_only, "esp32dev")
        print(f"✓ Found {library_analysis['external_count']} external libraries")
    except Exception as e:
        logger.warning(f"Library analysis failed: {e}. Using fallback.")
        library_analysis = {
            "external_count": 0,
            "builtin_count": 0,
            "unknown_count": 0,
            "external_libraries": [],
            "builtin_libraries": [],
            "unknown_libraries": []
        }
    
    # 3. Code quality (WRAPPED with fallback)
    try:
        quality_analysis = mcp_client.analyze_code_quality(code_only, "esp32dev")
        print(f"✓ Code quality score: {quality_analysis['quality_score']}/100")
        print(f"   Severity: {quality_analysis.get('severity', 'unknown')}")
    except Exception as e:
        logger.warning(f"Code quality analysis failed: {e}. Using fallback.")
        quality_analysis = {
            "quality_score": 0,
            "issues": [],
            "warnings": [],
            "estimated_ram_usage_percent": 0,
            "severity": "unknown",
            "summary": "Analysis unavailable"
        }
    
    # COMPILE CODE
    compile_start = time.time()
    if request.compile:
        local_success = False
        board_key = (request.board or "esp32dev").lower()
        board_map = {
            "uno": "uno",
            "nano": "nano",
            "esp32": "esp32",
            "esp32dev": "esp32",
            "esp32devkit": "esp32",
            "default": "esp32"
        }
        board_key = board_map.get(board_key, "esp32")
        fqbn = ARDUINO_BOARD_MAP.get(board_key, ARDUINO_BOARD_MAP["default"])
        try:
            print("\nPreflight checks...")
            preflight = preflight_check_arduino()
            
            if not preflight["arduino_cli_found"]:
                # Arduino CLI not available - skip compilation but show instructions
                compilation_status = "skipped"
                compilation_output = preflight["status_message"]
                compilation_error_summary = "arduino-cli not installed"
                compiler_used = "local"
                print(f"WARNING: {compilation_error_summary}")
            else:
                print(preflight["status_message"])
                
                if preflight["install_commands"]:
                    print("Run these commands to install missing cores:")
                    for cmd in preflight["install_commands"]:
                        print(f"  - {cmd}")
                
                # Save as Arduino sketch (.ino)
                sketch_dir, sketch_file = save_sketch_as_ino(code_only, request.description)
                print(f"Sketch saved for Arduino CLI: {sketch_file}")

                # Determine target board FQBN from request.board
                print(f"  Target board: {board_key} -> FQBN: {fqbn}")

                # Best-effort: attempt to install detected libraries before compiling
                initial_dependency_report = None
                if detected_libraries:
                    initial_dependency_report = install_libraries_with_arduino_cli(detected_libraries)
                    print(
                        f"  Library install attempt: {len(initial_dependency_report.get('installed', []))} installed, "
                        f"{len(initial_dependency_report.get('failed', []))} failed"
                    )

                # Compile with retries; compile_with_retries will auto-install missing headers and attach a dependency_report
                compile_result = compile_with_retries(sketch_dir, fqbn, detected_libraries or [], max_retries=2, initial_dependency_report=initial_dependency_report)
                compilation_output = compile_result.get("output")
                dependency_report = compile_result.get("dependency_report", initial_dependency_report)

                if compile_result.get("success"):
                    compilation_status = "success"
                    compiler_used = "local"
                    local_success = True
                    print("Compilation successful!")
                else:
                    compilation_status = "failed"
                    compiler_used = "local"
                    print("Compilation failed")
                    # Print full compilation output for debugging
                    if compilation_output:
                        print("\n=== COMPILATION ERROR DETAILS ===")
                        print(compilation_output[-2000:])  # Last 2000 chars
                        print("=== END DETAILS ===")
                    
                    # Check for LEDC API errors and attempt auto-repair
                    error_dict = parse_compilation_errors(compilation_output)
                    if error_dict.get("ledc_api_errors"):
                        print("\nDetected LEDC API error - attempting auto-repair...")
                        repaired_code = repair_ledc_api_code(code_only, compilation_output)
                        
                        # Save repaired code to sketch file
                        with open(sketch_file, "w", encoding="utf-8") as f:
                            f.write(repaired_code)
                        print("  Code repaired and saved")
                        
                        # Retry compilation with repaired code
                        print("  Retrying compilation with repaired code...")
                        compile_result = arduino_compile_sketch(sketch_dir, fqbn, detected_libraries)
                        compilation_output = compile_result.get("output")
                        
                        if compile_result.get("success"):
                            compilation_status = "success"
                            compiler_used = "local"
                            local_success = True
                            print("  Compilation successful after repair!")
                            code_only = repaired_code  # Update code_only with repaired version
                        else:
                            compilation_status = "failed"
                            compiler_used = "local"
                            print("  Compilation still failed after repair")

                # Error summary + troubleshooting
                if compilation_output:
                    error_dict = parse_compilation_errors(compilation_output)
                    error_counts = {k: len(v) for k, v in error_dict.items()}
                    error_summary = (
                        f"Syntax: {error_counts['syntax_errors']}, "
                        f"Missing Headers: {error_counts['missing_headers']}, "
                        f"Undefined Refs: {error_counts['undefined_references']}, "
                        f"Type Errors: {error_counts['type_errors']}, "
                        f"LEDC API: {error_counts.get('ledc_api_errors', 0)}, "
                        f"Other: {error_counts['other_errors']}"
                    )
                    troubleshooting_suggestions = generate_troubleshooting_suggestions(error_dict)

                # Short human-readable compilation error summary (first error lines)
                compilation_error_summary = None
                if compilation_output:
                    lines = [l.strip() for l in compilation_output.splitlines() if l.strip()]
                    errs = [l for l in lines if "error" in l.lower() or "fatal" in l.lower()]
                    if errs:
                        compilation_error_summary = " | ".join(errs[:3])
                    else:
                        compilation_error_summary = (lines[0][:300] + "...") if lines else None

                compiled_binary_path = compile_result.get("binary_path")
        except Exception as e:
            compilation_status = "failed"
            compiler_used = "local"
            compilation_output = f"Local compilation exception: {str(e)}"
            compilation_error_summary = "local compilation exception"

        # Remote fallback if local compilation failed or was skipped
        if not local_success:
            compiler_used = "remote"
            try:
                import requests
                remote_url = "http://127.0.0.1:8001/compile"
                remote_payload = {
                    "code": code_only,
                    "board": fqbn
                }
                remote_resp = requests.post(remote_url, json=remote_payload, timeout=120)
                remote_resp.raise_for_status()
                remote_json = remote_resp.json()

                if remote_json.get("success"):
                    compilation_status = "success"
                    compilation_output = remote_json.get("output", "")
                    compilation_error_summary = None
                    error_summary = None
                    troubleshooting_suggestions = []
                    compiler_used = "remote"
                else:
                    compilation_status = "failed"
                    compilation_output = remote_json.get("error", "Remote compile failed")
                    compilation_error_summary = "remote compilation failed"
                    compiler_used = "remote"
            except Exception as e:
                compilation_status = "failed"
                compiler_used = "remote"
                remote_error = f"Remote compilation exception: {str(e)}"
                if compilation_output:
                    compilation_output = f"{compilation_output}\\n\\n{remote_error}"
                else:
                    compilation_output = remote_error
                compilation_error_summary = "remote compilation exception"

        compile_success = compilation_status == "success"
        compilation_time = time.time() - compile_start
    else:
        compile_success = None
        compilation_time = 0.0

    # --- NEW: Enhanced Documentation Sections ---
    flash_usage_percent = None
    ram_usage_from_compile = None
    if compilation_output:
        flash_match = re.search(r"Sketch uses .*?\\((\\d+)%\\)", compilation_output)
        ram_match = re.search(r"Global variables use .*?\\((\\d+)%\\)", compilation_output)
        if flash_match:
            flash_usage_percent = float(flash_match.group(1))
        if ram_match:
            ram_usage_from_compile = float(ram_match.group(1))

    documentation_metadata = {
        "generation_time": f"{generation_time:.2f}s",
        "compilation_time": f"{compilation_time:.2f}s",
        "memory_usage": f"{quality_analysis.get('estimated_ram_usage_percent')}%" if quality_analysis.get("estimated_ram_usage_percent") is not None else "N/A",
        "flash_usage": f"{flash_usage_percent}%" if flash_usage_percent is not None else "N/A",
        "ram_usage": f"{ram_usage_from_compile}%" if ram_usage_from_compile is not None else (
            f"{quality_analysis.get('estimated_ram_usage_percent')}%" if quality_analysis.get("estimated_ram_usage_percent") is not None else "N/A"
        ),
        "lines_of_code": lines_of_code,
        "code_quality_score": quality_analysis.get("quality_score", "N/A"),
        "optimization_notes": "Prefer millis()-based scheduling and reduce blocking delays where possible."
    }

    # --- NEW: Generate Circuit Diagram Assets (Always) ---
    diagram_assets = docs_generator.generate_diagram_assets(code_only)
    mermaid_code = diagram_assets.get("mermaid_code")
    mermaid_url = diagram_assets.get("diagram_url")
    
    # GENERATE DOCUMENTATION (Phase 7: Enhanced) - CONDITIONAL
    if request.generate_docs:
        print(f"\nGenerating comprehensive documentation (Phase 7)...")
        try:

            # Use Phase 7 Documentation Generator
            doc_content = docs_generator.generate_full_documentation(
                code=code_only,
                description=request.description,
                libraries=[lib for lib, _ in detected_libraries] if detected_libraries else [],
                metadata=documentation_metadata
            )

            if doc_content:
                doc_path = save_documentation(doc_content, filepath)
                documentation = doc_content
                print(f"Documentation generated ({len(doc_content)} chars)")
                logger.info(f"Documentation generated: {len(doc_content)} characters")
        except Exception as e:
            error_msg = f"Doc generation error: {str(e)}"
            print(f"WARNING: {error_msg}")
            logger.error(error_msg)
            documentation = f"# {request.description}\n\nDocumentation generation encountered an error. Please refer to the generated code."

    # --- NEW: Evaluation Metrics ---
    EVAL_METRICS["total_requests"] += 1
    EVAL_METRICS["quality_score_total"] += float(quality_analysis.get("quality_score", 0))

    if request.compile:
        EVAL_METRICS["compile_attempts"] += 1
        if compile_success:
            EVAL_METRICS["compile_successes"] += 1

    if EVAL_METRICS["compile_attempts"] > 0:
        compilation_success_rate = round(
            (EVAL_METRICS["compile_successes"] / EVAL_METRICS["compile_attempts"]) * 100.0, 2
        )
    else:
        compilation_success_rate = None

    average_quality_score = round(
        EVAL_METRICS["quality_score_total"] / max(1, EVAL_METRICS["total_requests"]), 2
    )

    ram_usage_percent = quality_analysis.get("estimated_ram_usage_percent")
    if ram_usage_percent is not None:
        memory_efficiency_score = round(max(0.0, 100.0 - float(ram_usage_percent)), 2)

    evaluation_summary = (
        f"gen_time={generation_time:.2f}s, "
        f"compile_time={compilation_time:.2f}s, "
        f"compile_success={compile_success}, "
        f"loc={lines_of_code}, "
        f"avg_quality={average_quality_score}, "
        f"compile_success_rate={compilation_success_rate}"
    )
    
    print(f"\n{'='*70}\n")
    
    return CodeGenerationResponse(
        description=request.description,
        generated_code=code_only,
        file_path=filepath,
        success=compile_success,
        compile_success=compile_success,
        compilation_status=compilation_status,
        compilation_output=compilation_output if compilation_output else None,
        compiler=compiler_used,
        generation_time=round(generation_time, 3),
        compilation_time=round(compilation_time, 3),
        lines_of_code=lines_of_code,
        compilation_success_rate=compilation_success_rate,
        average_quality_score=average_quality_score,
        memory_efficiency_score=memory_efficiency_score,
        flash_usage_percent=flash_usage_percent,
        ram_usage_percent=ram_usage_from_compile if ram_usage_from_compile is not None else quality_analysis.get('estimated_ram_usage_percent'),
        evaluation_summary=evaluation_summary,
        mermaid_code=mermaid_code,
        mermaid_url=mermaid_url,
        compilation_error_summary=compilation_error_summary,
        compiled_binary_path=compiled_binary_path,
        detected_libraries=[f"{h} -> {l}" for h, l in detected_libraries] if detected_libraries else None,
        error_summary=error_summary,
        troubleshooting_suggestions=troubleshooting_suggestions if troubleshooting_suggestions else None,
        documentation=documentation,
        installation_guide=installation_guide,
        dependency_report=dependency_report,
        hardware_info=hardware_specs,
        code_quality_score=quality_analysis['quality_score'],
        memory_usage=quality_analysis.get('estimated_ram_usage_percent'),
        quality_issues=quality_analysis.get('issues', []),
        quality_warnings=quality_analysis.get('warnings', [])
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

