#!/usr/bin/env python3
"""
Compile Smoke Test - Verify Arduino CLI works with sample ESP32 + Uno sketches.

Usage:
  python scripts/compile_smoke_test.py
  python scripts/compile_smoke_test.py --board esp32
  python scripts/compile_smoke_test.py --board uno
  python scripts/compile_smoke_test.py --board all
"""

import os
import sys
import subprocess
import io

# Fix Windows terminal encoding
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import tempfile
import argparse
import shutil
from pathlib import Path

# Add parent dir to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_arduino_cli():
    """Get arduino-cli path."""
    return shutil.which("arduino-cli")

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_section(text):
    """Print section marker."""
    print(f"\n>>> {text}")

def ensure_cores():
    """Ensure required cores are installed."""
    arduino = get_arduino_cli()
    if not arduino:
        print("❌ arduino-cli not found")
        return False
    
    print_section("Ensuring cores installed...")
    
    for platform in ["esp32:esp32", "arduino:avr"]:
        try:
            # Update index
            cmd = [arduino, "core", "update-index"]
            subprocess.run(cmd, capture_output=True, timeout=120)
            
            # Install core
            cmd = [arduino, "core", "install", platform]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"  ✓ {platform}")
            else:
                print(f"  ⚠️  {platform}: {result.stderr[:100]}")
        except Exception as e:
            print(f"  ⚠️  {platform}: {str(e)}")
    
    return True

def create_sketch(temp_dir, name, fqbn):
    """Create a test sketch."""
    sketch_dir = os.path.join(temp_dir, name)
    os.makedirs(sketch_dir, exist_ok=True)
    
    # Determine code based on FQBN
    if "esp32" in fqbn:
        code = """
void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  Serial.println("ESP32 Blink started");
}

void loop() {
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(500);
}
"""
    else:  # Arduino AVR
        code = """
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.println("Arduino Blink started");
}

void loop() {
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}
"""
    
    sketch_file = os.path.join(sketch_dir, f"{name}.ino")
    with open(sketch_file, "w") as f:
        f.write(code)
    
    return sketch_dir, sketch_file

def compile_sketch(arduino, sketch_dir, fqbn):
    """Compile a sketch. Returns tuple (success, output, binary_path)."""
    build_dir = os.path.join(sketch_dir, "build")
    cmd = [
        arduino, "compile",
        "--fqbn", fqbn,
        sketch_dir,
        "--build-path", build_dir,
        "--verbose"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
        
        # Find binary
        binary_path = None
        if os.path.exists(build_dir):
            for root, dirs, files in os.walk(build_dir):
                for f in files:
                    if f.endswith((".bin", ".hex", ".elf")):
                        binary_path = os.path.join(root, f)
                        break
                if binary_path:
                    break
        
        return result.returncode == 0, output, binary_path
    except subprocess.TimeoutExpired:
        return False, "⏱ Compilation timeout", None
    except Exception as e:
        return False, f"❌ Error: {str(e)}", None

def run_test(board_name, fqbn):
    """Run a single compile test."""
    print_header(f"Testing {board_name} ({fqbn})")
    
    arduino = get_arduino_cli()
    if not arduino:
        print("❌ arduino-cli not found")
        return False
    
    print(f"Tool: {arduino}\n")
    
    # Create temp sketch
    with tempfile.TemporaryDirectory() as temp_dir:
        sketch_name = f"blink_{board_name}_test"
        print_section(f"Creating sketch: {sketch_name}")
        sketch_dir, sketch_file = create_sketch(temp_dir, sketch_name, fqbn)
        print(f"✓ Sketch created: {sketch_file}")
        
        print_section("Compiling...")
        success, output, binary = compile_sketch(arduino, sketch_dir, fqbn)
        
        if success:
            print("✓ Compilation SUCCESSFUL\n")
            if binary:
                size = os.path.getsize(binary)
                print(f"✓ Binary created: {os.path.basename(binary)} ({size} bytes)")
        else:
            print("❌ Compilation FAILED\n")
        
        print_section("Compilation Output")
        # Print last 50 lines of output
        lines = output.splitlines()
        relevant_lines = lines[-50:] if len(lines) > 50 else lines
        for line in relevant_lines:
            print(line)
        
        return success

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Compile smoke test for Arduino CLI")
    parser.add_argument("--board", choices=["esp32", "uno", "all"], default="all",
                        help="Board to test (default: all)")
    args = parser.parse_args()
    
    print_header("Arduino CLI Compile Smoke Test")
    
    # Check arduino-cli
    arduino = get_arduino_cli()
    if not arduino:
        print("\n❌ FATAL: arduino-cli not found on PATH")
        print("\nInstall with:")
        print("  Chocolatey: choco install arduino-cli")
        print("  Scoop: scoop install arduino-cli")
        print("  Manual: https://github.com/arduino/arduino-cli/releases")
        sys.exit(1)
    
    print(f"✓ arduino-cli found: {arduino}\n")
    
    # Ensure cores
    if not ensure_cores():
        print("\n⚠️  Core installation had issues but continuing anyway...")
    
    # Run tests
    tests = {
        "esp32": ("esp32:esp32:esp32", "ESP32 DevKit"),
        "uno": ("arduino:avr:uno", "Arduino Uno")
    }
    
    if args.board == "all":
        boards_to_test = ["esp32", "uno"]
    else:
        boards_to_test = [args.board]
    
    results = {}
    for board_key in boards_to_test:
        fqbn, name = tests[board_key]
        results[board_key] = run_test(name, fqbn)
    
    # Summary
    print_header("Test Summary")
    for board_key, success in results.items():
        status = "✓ PASS" if success else "❌ FAIL"
        print(f"  {board_key}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
