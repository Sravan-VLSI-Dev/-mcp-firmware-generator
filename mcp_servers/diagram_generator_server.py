import re
import base64
import zlib
import json


class DiagramGenerator:

    def extract_pins(self, code: str):
        """
        Extract pin definitions from the provided code.
        Supports 'const int', '#define', and direct pinMode() usage patterns.
        """
        components = []
        used_pins = set()

        # Match const int or int variable assignment
        var_pattern = r'(?:const\s+)?int\s+(\w+)\s*=\s*(\d+);'
        var_matches = re.findall(var_pattern, code)

        for name, pin in var_matches:
            components.append({
                "name": name,
                "pin": pin
            })
            used_pins.add(int(pin))

        # Match #define pattern
        define_pattern = r'#define\s+(\w+)\s+(\d+)'
        define_matches = re.findall(define_pattern, code)

        for name, pin in define_matches:
            components.append({
                "name": name,
                "pin": pin
            })
            used_pins.add(int(pin))

        # Match direct pinMode usage (e.g., pinMode(2, OUTPUT))
        pinMode_pattern = r'pinMode\s*\(\s*(\d+)\s*,\s*(?:OUTPUT|INPUT|INPUT_PULLUP)\s*\)'
        pinMode_matches = re.findall(pinMode_pattern, code)

        for pin in pinMode_matches:
            pin_num = int(pin)
            if pin_num not in used_pins:
                # Create a generic name for directly used pins
                components.append({
                    "name": f"pin{pin_num}",
                    "pin": str(pin_num)
                })
                used_pins.add(pin_num)

        return components


    def generate_mermaid(self, components):
        """
        Convert extracted components into Mermaid diagram syntax.
        """
        diagram = "graph TD\n"
        diagram += "    ESP32\n"

        for comp in components:
            clean_name = comp["name"].replace("Pin", "")
            diagram += f"    ESP32 -->|GPIO {comp['pin']}| {clean_name}\n"

        return diagram

    def generate_mermaid_url(self, mermaid_code: str) -> str:
        """
        Generate Mermaid Live URL using simple base64 JSON encoding.
        No compression required.
        """

        payload = {
            "code": mermaid_code,
            "mermaid": {
                "theme": "default"
            }
        }

        json_str = json.dumps(payload)

        encoded = base64.urlsafe_b64encode(
            json_str.encode("utf-8")
        ).decode("utf-8")

        return f"https://mermaid.live/edit#{encoded}"
