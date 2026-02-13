from mcp_servers.diagram_generator_server import DiagramGenerator
import json
import base64

sample_code = """
const int ledPin = 2;
const int buzzerPin = 5;
const int sensorPin = 34;
"""

diagram_gen = DiagramGenerator()

components = diagram_gen.extract_pins(sample_code)
print("Extracted Components:")
print(components)

mermaid_code = diagram_gen.generate_mermaid(components)
print("\nGenerated Mermaid Code:")
print(mermaid_code)

url = diagram_gen.generate_mermaid_url(mermaid_code)
print("\nGenerated Mermaid URL:")
print(url)

def generate_mermaid_url(mermaid_code: str) -> str:
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