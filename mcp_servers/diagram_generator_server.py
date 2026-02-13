import re
import base64
import zlib
import json


class DiagramGenerator:

    def extract_pins(self, code: str):
        """
        Extract pin definitions from the provided code.
        Supports both 'const int' and '#define' patterns.
        """
        components = []

        # Match const int or int variable assignment
        var_pattern = r'(?:const\s+)?int\s+(\w+)\s*=\s*(\d+);'
        var_matches = re.findall(var_pattern, code)

        for name, pin in var_matches:
            components.append({
                "name": name,
                "pin": pin
            })

        # Match #define pattern
        define_pattern = r'#define\s+(\w+)\s+(\d+)'
        define_matches = re.findall(define_pattern, code)

        for name, pin in define_matches:
            components.append({
                "name": name,
                "pin": pin
            })

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
