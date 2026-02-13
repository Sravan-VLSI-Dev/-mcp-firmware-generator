#!/usr/bin/env python3
"""
Documentation Generator Server - Enhanced technical documentation output.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from mcp_servers.diagram_generator_server import DiagramGenerator


class DocsGeneratorServer:
    """Generate publication-ready embedded systems documentation."""

    def __init__(self, host: str = None, model: str = None):
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3:latest")
        try:
            import ollama
            self.client = ollama.Client(host=self.host)
            self.has_ollama = True
        except ImportError:
            self.client = None
            self.has_ollama = False

    # --- NEW: Enhanced Documentation Sections ---
    def _extract_includes(self, code: str) -> List[str]:
        return re.findall(r'#include\s+[<"]([^>"]+)[>"]', code)

    def _extract_components(self, code: str) -> List[Dict[str, str]]:
        generator = DiagramGenerator()
        return generator.extract_pins(code)

    def _component_name(self, variable_name: str, includes: List[str]) -> str:
        key = (variable_name or "").lower()
        include_set = {inc.lower() for inc in includes}

        keyword_map = [
            ("led", "LED"),
            ("buzzer", "Buzzer"),
            ("dht", "DHT22"),
            ("relay", "Relay"),
            ("servo", "Servo"),
            ("button", "Button"),
            ("switch", "Switch"),
            ("pir", "PIR Sensor"),
            ("ldr", "LDR Sensor"),
            ("mq", "Gas Sensor"),
            ("trig", "Ultrasonic Trigger"),
            ("echo", "Ultrasonic Echo"),
            ("sda", "I2C SDA"),
            ("scl", "I2C SCL"),
        ]

        include_map = [
            ("dht.h", "DHT22"),
            ("wifi.h", "WiFi Module"),
            ("pubsubclient.h", "MQTT Module"),
            ("bluetoothserial.h", "Bluetooth Module"),
            ("bledevice.h", "BLE Module"),
            ("onewire.h", "OneWire Sensor"),
            ("dallastemperature.h", "DS18B20"),
            ("bmp280.h", "BMP280"),
        ]

        for pattern, label in keyword_map:
            if pattern in key:
                return label

        for include_name, label in include_map:
            if include_name in include_set:
                return label

        normalized = re.sub(r"(_|PIN|Pin)", " ", variable_name or "Component")
        return re.sub(r"\s+", " ", normalized).strip() or "Component"

    def _component_mode(self, component_name: str) -> str:
        lowered = component_name.lower()
        output_like = ["led", "buzzer", "relay", "servo", "motor", "pump", "fan"]
        if any(token in lowered for token in output_like):
            return "OUTPUT"
        return "INPUT"

    def _component_description(self, component_name: str) -> str:
        desc_map = {
            "led": "Status indicator",
            "buzzer": "Audible alert output",
            "dht22": "Temperature and humidity sensing",
            "relay": "High-power switching output",
            "servo": "Position control actuator",
            "button": "Digital user input",
            "switch": "Binary user input",
            "wifi": "Network connectivity",
            "mqtt": "Message broker communication",
            "pir": "Motion detection",
            "ldr": "Ambient light sensing",
            "gas": "Gas concentration sensing",
        }
        lowered = component_name.lower()
        for key, value in desc_map.items():
            if key in lowered:
                return value
        return "GPIO-connected peripheral"

    def _library_reason(self, include_name: str) -> str:
        reasons = {
            "arduino.h": "Core Arduino framework APIs and startup definitions.",
            "wifi.h": "ESP32 WiFi stack for network connectivity.",
            "wire.h": "I2C bus communication for digital peripherals.",
            "spi.h": "SPI bus communication for high-speed peripherals.",
            "dht.h": "DHT-series temperature/humidity sensor driver.",
            "pubsubclient.h": "MQTT publish/subscribe communication.",
            "bluetoothserial.h": "Classic Bluetooth serial transport.",
            "bledevice.h": "Bluetooth Low Energy device roles and services.",
            "onewire.h": "OneWire bus handling.",
            "dallastemperature.h": "DS18B20 temperature sensor abstraction.",
        }
        return reasons.get(include_name.lower(), "Library dependency required by referenced APIs.")

    def generate_diagram_assets(self, code: str) -> Dict[str, Optional[str]]:
        includes = self._extract_includes(code)
        components = self._extract_components(code)
        if not components:
            return {"mermaid_code": None, "diagram_url": None}

        labeled_components = []
        for comp in components:
            base = self._component_name(comp.get("name", ""), includes)
            mode = self._component_mode(base)
            semantic = f"{base} ({'Digital Output' if mode == 'OUTPUT' else 'Sensor/Input'})"
            labeled_components.append({"name": semantic, "pin": comp.get("pin")})

        generator = DiagramGenerator()
        mermaid_code = generator.generate_mermaid(labeled_components)
        diagram_url = generator.generate_mermaid_url(mermaid_code)
        return {"mermaid_code": mermaid_code, "diagram_url": diagram_url}

    def _architecture_mermaid(self) -> str:
        return (
            "graph TD\n"
            "    UI[Static Frontend] --> API[FastAPI Backend]\n"
            "    API --> LLM[Ollama LLM]\n"
            "    API --> MCP[MCP Servers]\n"
            "    API --> CLI[Arduino CLI]\n"
            "    MCP --> DOCS[Documentation Generator]\n"
            "    MCP --> DIAG[Diagram Generator]\n"
            "    CLI --> BIN[Compiled Firmware Artifact]\n"
        )

    def _pin_table_markdown(self, code: str) -> str:
        includes = self._extract_includes(code)
        components = self._extract_components(code)

        lines = [
            "| Component | GPIO | Mode | Description |",
            "|---|---:|---|---|",
        ]

        for comp in components:
            component_name = self._component_name(comp.get("name", ""), includes)
            mode = self._component_mode(component_name)
            description = self._component_description(component_name)
            lines.append(f"| {component_name} | {comp.get('pin')} | {mode} | {description} |")

        if len(lines) == 2:
            lines.append("| N/A | N/A | N/A | No explicit GPIO mapping found |")

        return "\n".join(lines)

    def _library_installation_section(self, includes: List[str]) -> str:
        if not includes:
            return "No include directives were detected."

        sections = []
        for include_name in sorted(set(includes)):
            sections.append(f"### {include_name}")
            sections.append(self._library_reason(include_name))
            sections.append("")
            sections.append("Arduino CLI:")
            sections.append("```bash")
            sections.append(f"arduino-cli lib install {include_name.replace('.h', '')}")
            sections.append("```")
            sections.append("")
            sections.append("Arduino IDE:")
            sections.append("1. Open Library Manager.")
            sections.append(f"2. Search for `{include_name.replace('.h', '')}`.")
            sections.append("3. Install latest compatible version.")
            sections.append("")

        return "\n".join(sections)

    def _code_walkthrough(self, code: str) -> str:
        has_interrupt = "attachInterrupt" in code
        has_non_blocking = ("millis(" in code) and ("delay(" not in code or "unsigned long" in code)

        parts = [
            "### Global Variables",
            "Global state includes sensor objects, communication clients, and runtime control variables.",
            "",
            "### Pin Definitions",
            "Pin constants map peripherals to ESP32 GPIOs and isolate hardware mapping from logic.",
            "",
            "### setup() Function",
            "Performs hardware initialization, serial startup, peripheral configuration, and one-time subsystem bootstrapping.",
            "",
            "### loop() Function",
            "Executes the runtime control loop: sensor acquisition, decision logic, actuator update, and communication output.",
            "",
            "### Interrupts (if any)",
            "Interrupt handlers are configured and used for asynchronous event capture." if has_interrupt else "No interrupt handlers detected in the generated firmware.",
            "",
            "### Communication Logic",
            "Implements serial/network protocol flow for telemetry, commands, and status feedback.",
            "",
            "### Error Handling",
            "Includes guard conditions for invalid sensor reads, startup failures, and communication retries.",
            "",
            "### Non-blocking Timing",
            "Uses millis()-based scheduling for cooperative timing and responsiveness." if has_non_blocking else "Uses delay-based pacing; can be upgraded to millis()-based scheduling for better responsiveness.",
        ]
        return "\n".join(parts)

    def generate_full_documentation(
        self,
        code: str,
        description: str,
        libraries: List[str] = None,
        metadata: Optional[Dict] = None,
    ) -> str:
        """Generate enhanced technical documentation in fixed section order."""

        # --- NEW: Enhanced Documentation Sections ---
        metadata = metadata or {}
        includes = libraries[:] if libraries else self._extract_includes(code)
        diagram_assets = self.generate_diagram_assets(code)
        circuit_mermaid = diagram_assets.get("mermaid_code") or "graph TD\n    ESP32"

        code_generation_time = metadata.get("generation_time", "N/A")
        compilation_time = metadata.get("compilation_time", "N/A")
        memory_usage = metadata.get("memory_usage", "N/A")
        flash_usage = metadata.get("flash_usage", "N/A")
        ram_usage = metadata.get("ram_usage", metadata.get("memory_usage", "N/A"))
        lines_of_code = metadata.get("lines_of_code", "N/A")
        quality_score = metadata.get("code_quality_score", "N/A")
        optimization_notes = metadata.get("optimization_notes", "No specific optimizations reported.")

        architecture_mermaid = self._architecture_mermaid()
        pin_table = self._pin_table_markdown(code)
        library_section = self._library_installation_section(includes)
        walkthrough = self._code_walkthrough(code)

        doc = f"""# {description}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Project Overview

Problem statement:
Current embedded firmware projects need repeatable, AI-assisted generation plus deterministic compile validation.

Objective:
Generate production-ready ESP32 firmware from requirements, validate dependencies, compile, and document results.

Target microcontroller:
ESP32 (default target profile), with board mapping handled in backend.

System workflow explanation:
Request -> code generation -> validation -> library detection -> compilation -> quality analysis -> documentation output.

AI + compilation pipeline summary:
FastAPI orchestrates Ollama inference, MCP analyses, and Arduino CLI compile checks in one flow.

## 2. System Architecture

High-level components:
- Frontend: static web app for prompt input and result visualization.
- FastAPI backend: orchestration, validation, retries, and response assembly.
- LLM (Ollama): firmware code generation.
- MCP servers: hardware and quality analysis + documentation helpers.
- Arduino CLI: deterministic compilation and diagnostics.

```mermaid
{architecture_mermaid}
```

## 3. Hardware Requirements

- Microcontroller board: ESP32 DevKit V1 or compatible.
- Sensors: determined by include set and pin mappings in generated firmware.
- Actuators: derived from output pin assignments (e.g., LED, buzzer, relay, motor).
- Communication modules: WiFi/BLE/MQTT modules as required by include set.
- Power requirements: stable 5V USB input; ensure 3.3V GPIO-level-safe peripherals.

## 4. Pin Configuration Table

{pin_table}

## 5. Circuit Diagram (Embedded)

```mermaid
{circuit_mermaid}
```

## 6. Library Installation Guide

{library_section}

## 7. Code Walkthrough (Detailed)

{walkthrough}

## 8. Compilation & Performance Metrics

Code Generation Time: {code_generation_time}
Compilation Time: {compilation_time}
Memory Usage: {memory_usage}
Flash Usage: {flash_usage}
RAM Usage: {ram_usage}
Lines of Code: {lines_of_code}
Optimization Notes: {optimization_notes}

## 9. Quality Analysis

- Code readability assessment: quality score reported as {quality_score}.
- Modularity score: inferred from function boundaries and responsibility separation.
- Embedded best practices followed: setup/loop structure, GPIO abstraction, and compile validation.
- Safety evaluation: GPIO voltage assumptions and peripheral usage must match board constraints.
- Potential improvements: stricter non-blocking patterns, stronger fault recovery, and structured telemetry.

## 10. Troubleshooting Guide (Expanded)

- Compilation errors: verify board FQBN, include directives, and Arduino core installation.
- Missing libraries: install dependencies via Arduino CLI or IDE library manager.
- Board mismatch: ensure selected board and FQBN map to target hardware.
- Serial monitor issues: confirm COM port, baud rate, and cable supports data.
- Power instability issues: use stable power supply and avoid overloading GPIO current limits.

## 11. Future Improvements

- OTA firmware updates.
- RTOS task-based scheduling.
- Power optimization and sleep-state orchestration.
- Web dashboard for telemetry and control.
- Cloud logging and remote observability.
- Hardware abstraction layers for board portability.
"""

        return doc


if __name__ == "__main__":
    sample_code = """
#include <WiFi.h>
#define LED_PIN 2
#define DHT_PIN 23
void setup(){ pinMode(LED_PIN, OUTPUT); }
void loop(){ digitalWrite(LED_PIN, HIGH); delay(1000); }
"""
    server = DocsGeneratorServer()
    print(server.generate_full_documentation(sample_code, "Sample Project"))
