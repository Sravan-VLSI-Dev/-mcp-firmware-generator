#!/usr/bin/env python3
"""
Code Quality MCP Server
Analyzes generated code for structure, safety, and best practices
"""

import re
import json
from typing import List, Dict, Tuple

# Try importing MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("⚠ MCP not installed. Running in standalone mode.")

# ============================================================================
# BOARD SPECIFICATIONS (Exportable for mcp_client.py)
# ============================================================================

BOARD_SPECS = {
    "esp32dev": {"total_ram": 520, "system_reserve": 100},
    "esp32s3": {"total_ram": 1507, "system_reserve": 150},
    "esp32c3": {"total_ram": 400, "system_reserve": 80}
}

# ============================================================================
# CODE QUALITY ANALYZER
# ============================================================================

class CodeQualityAnalyzer:
    """Analyzes C/C++ code for quality issues."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.quality_score = 100
    
    def analyze(self, code: str, board: str = "esp32dev") -> Dict:
        """Run full analysis on code."""
        self.code = code  # ← CRITICAL FIX: Store code for use in check methods
        self.board = board  # Store board for memory estimation
        self.issues = []
        self.warnings = []
        self.quality_score = 100
        
        # Run all checks
        self._check_setup_loop()
        self._check_serial_init()
        self._check_memory_safety()
        self._check_blocking_calls()
        self._check_error_handling()
        self._check_best_practices()
        self._estimate_memory(board)
        
        # Calculate score
        self.quality_score = max(0, 100 - (len(self.issues) * 15 + len(self.warnings) * 5))
        
        return {
            "code_lines": len(code.split('\n')),
            "code_size_kb": len(code) / 1024,
            "quality_score": self.quality_score,
            "issues": self.issues,
            "warnings": self.warnings,
            "issues_count": len(self.issues),
            "warnings_count": len(self.warnings),
            "severity": self._get_severity(),
            "summary": self._get_summary(),
            "estimated_ram_usage_percent": self._estimate_ram_usage(board)
        }
    
    def _check_setup_loop(self):
        """Check for required setup() and loop() functions."""
        code = self.code
        
        if "void setup()" not in code and "void setup (" not in code:
            self.issues.append("Missing void setup() function - code won't compile")
            return
        
        if "void loop()" not in code and "void loop (" not in code:
            self.issues.append("Missing void loop() function - code won't compile")
            return
    
    def _check_serial_init(self):
        """Check for Serial initialization."""
        code = self.code
        
        if "Serial.begin" not in code:
            self.warnings.append("Missing Serial.begin() - debugging and monitoring will be difficult")
    
    def _check_memory_safety(self):
        """Check for potential memory issues."""
        code = self.code
        
        # Check for unbounded arrays
        if re.search(r'char\s+\w+\s*\[\s*\]', code):
            self.warnings.append("Unbounded array declaration detected - may cause memory issues")
        
        # Check for large static allocations
        if re.search(r'char\s+\w+\s*\[\s*\d{4,}\s*\]', code):
            self.issues.append("Large static array allocation (>1000 bytes) - verify memory available")
        
        # Check for dynamic allocation without free
        malloc_count = code.count('malloc')
        free_count = code.count('free')
        
        if malloc_count > 0 and malloc_count > free_count:
            self.warnings.append(
                f"Found {malloc_count} malloc calls but only {free_count} free calls - potential memory leak"
            )
    
    def _check_blocking_calls(self):
        """Check for blocking function calls."""
        code = self.code
        blocking_patterns = [
            (r'delay\s*\(\s*\d{5,}\s*\)', "Very long delay (>100ms) detected - will block entire system"),
            (r'while\s*\(\s*1\s*\)', "Infinite loop with while(1) - use loop() function instead"),
            (r'Serial\.println.*?\);', "Serial printing in loop without delay - may overwhelm serial"),
        ]
        
        for pattern, message in blocking_patterns:
            if re.search(pattern, code):
                self.warnings.append(message)
    
    def _check_error_handling(self):
        """Check for error handling."""
        code = self.code
        
        # Check for try-catch (not common in Arduino but good practice)
        has_error_check = 'if' in code or 'return' in code or 'try' in code
        
        # Check for assertion or validation
        if 'assert' not in code and code.count('if (') < 3:
            self.warnings.append("Limited error checking - code may fail silently on bad input")
    
    def _check_best_practices(self):
        """Check for best practices."""
        code = self.code
        
        # Check for const correctness
        if 'const' not in code:
            self.warnings.append("No const declarations found - consider using const for constants")
        
        # Check for comments
        comment_ratio = (code.count('//') + code.count('/*')) / max(1, len(code.split('\n')))
        if comment_ratio < 0.05:
            self.warnings.append("Low comment density (<5%) - consider adding more documentation")
        
        # Check for long functions
        function_pattern = r'(?:void|int|float|bool|uint\d+_t|double)\s+\w+\s*\([^)]*\)\s*\{'
        functions = re.findall(function_pattern, code)
        if len(functions) == 1:  # Just setup/loop
            self.warnings.append("Code is in main setup/loop - consider breaking into smaller functions")
    
    def _estimate_memory(self, board: str):
        """Estimate memory usage."""
        board_ram = {
            "esp32dev": 520,
            "esp32s3": 1507,
            "esp32c3": 400
        }
        
        ram_kb = board_ram.get(board, 520)
        code_size_kb = len(self.code) / 1024
        
        usage_percent = (code_size_kb / ram_kb) * 100
        
        if usage_percent > 80:
            self.issues.append(f"Code size ({code_size_kb:.1f}KB) is very large for {board}")
        elif usage_percent > 50:
            self.warnings.append(f"Code size ({code_size_kb:.1f}KB) uses >50% of available RAM")
    
    def _estimate_ram_usage(self, board: str) -> float:
        """Return RAM usage percentage."""
        board_ram = {
            "esp32dev": 520,
            "esp32s3": 1507,
            "esp32c3": 400
        }
        
        ram_kb = board_ram.get(board, 520)
        code_size_kb = len(self.code) / 1024
        usage_percent = (code_size_kb / ram_kb) * 100
        return round(usage_percent, 2)
    
    def _get_severity(self) -> str:
        """Get overall severity level."""
        if len(self.issues) > 3:
            return "critical"
        elif len(self.issues) > 0:
            return "high"
        elif len(self.warnings) > 3:
            return "medium"
        elif len(self.warnings) > 0:
            return "low"
        else:
            return "excellent"
    
    def _get_summary(self) -> str:
        """Get human-readable summary."""
        if self.quality_score >= 90:
            return "Excellent code quality - ready to use"
        elif self.quality_score >= 75:
            return "Good code quality - minor issues to address"
        elif self.quality_score >= 50:
            return "Moderate code quality - several issues to fix"
        else:
            return "Poor code quality - address critical issues before use"

# ============================================================================
# MEMORY ESTIMATION
# ============================================================================

def estimate_heap_usage(code: str, board: str) -> Dict:
    """Estimate heap memory usage."""
    
    # Count various memory allocations
    global_vars = len(re.findall(r'^\s*(int|float|double|char|bool|uint\d+_t)\s+\w+', code, re.MULTILINE))
    arrays = len(re.findall(r'\[\s*\d+\s*\]', code))
    structs = len(re.findall(r'(struct|typedef\s+struct)', code))
    
    estimated_global_kb = (global_vars * 4 + arrays * 20 + structs * 10) / 1024  # Very rough
    
    specs = BOARD_SPECS.get(board, BOARD_SPECS["esp32dev"])
    available = specs["total_ram"] - specs["system_reserve"] - (len(code) / 1024)
    
    return {
        "board": board,
        "estimated_code_size_kb": len(code) / 1024,
        "estimated_global_vars_kb": estimated_global_kb,
        "total_available_ram_kb": specs["total_ram"],
        "system_reserved_kb": specs["system_reserve"],
        "estimated_free_ram_kb": max(0, available),
        "usage_percent": min(100, ((len(code) / 1024) / specs["total_ram"]) * 100),
        "safety_margin": "good" if available > 50 else "warning" if available > 10 else "critical"
    }

# ============================================================================
# MCP SERVER SETUP
# ============================================================================

if HAS_MCP:
    server = Server("code-quality")
else:
    server = None

# ============================================================================
# MCP TOOL REGISTRATION
# ============================================================================

if HAS_MCP:
    @server.list_tools()
    async def list_tools():
        """List available tools."""
        return [
            Tool(
                name="analyze_code_quality",
                description="Analyze code for structure, safety, and best practices",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "C/C++ source code"},
                        "board": {
                            "type": "string",
                            "description": "Target board (esp32dev, esp32s3, esp32c3)"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="check_memory_usage",
                description="Estimate memory usage for target board",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "board": {"type": "string"}
                    },
                    "required": ["code", "board"]
                }
            ),
            Tool(
                name="get_code_metrics",
                description="Get various code metrics",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Source code"}
                    },
                    "required": ["code"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        """Execute tool calls."""
        code = arguments.get("code", "")
        board = arguments.get("board", "esp32dev")
        
        if name == "analyze_code_quality":
            analyzer = CodeQualityAnalyzer()
            analyzer.code = code
            result = analyzer.analyze(code, board)
        
        elif name == "check_memory_usage":
            result = estimate_heap_usage(code, board)
        
        elif name == "get_code_metrics":
            lines = code.split('\n')
            functions = len(re.findall(r'void\s+\w+\s*\(', code))
            variables = len(re.findall(r'(int|float|char|bool)\s+\w+', code))
            
            result = {
                "total_lines": len(lines),
                "non_empty_lines": len([l for l in lines if l.strip()]),
                "comment_lines": len([l for l in lines if l.strip().startswith('//')]),
                "function_count": functions,
                "variable_declarations": variables,
                "includes": len(re.findall(r'#include', code)),
                "complexity": "high" if functions > 10 else "medium" if functions > 3 else "low"
            }
        
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

# ============================================================================
# STANDALONE TEST MODE
# ============================================================================

async def run_mcp_server():
    """Run the MCP server via stdio."""
    if not HAS_MCP:
        print("❌ MCP SDK not installed. Install with: pip install mcp")
        return
    
    from mcp.server.stdio import stdio_server
    
    print("✓ Code Quality MCP Server starting...")
    print("  Ready to analyze code quality")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

# ============================================================================
# MAIN / TEST MODE
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    if HAS_MCP:
        print("\n" + "="*70)
        print("🔍 Code Quality MCP Server")
        print("="*70)
        asyncio.run(run_mcp_server())
    else:
        # Test mode
        print("\n" + "="*70)
        print("🔍 Code Quality Server (Test Mode - No MCP)")
        print("="*70)
        
        # Sample code to analyze
        sample_code = """
#include <WiFi.h>
#include <DHT.h>
#include <Wire.h>

#define DHT_PIN 32
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(115200);
    WiFi.begin("SSID", "PASSWORD");
    dht.begin();
}

void loop() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Failed to read from DHT sensor");
        return;
    }
    
    Serial.print("Temperature: ");
    Serial.println(temperature);
    
    delay(2000);
}
"""
        
        print("\n📊 Test 1: Code Quality Analysis")
        print("-" * 70)
        analyzer = CodeQualityAnalyzer()
        analyzer.code = sample_code
        analysis = analyzer.analyze(sample_code, "esp32dev")
        print(json.dumps(analysis, indent=2))
        
        print("\n📊 Test 2: Memory Usage Estimation")
        print("-" * 70)
        memory = estimate_heap_usage(sample_code, "esp32dev")
        print(json.dumps(memory, indent=2))
        
        print("\n✓ All tests completed!")
