from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class CodeGenerationRequest(BaseModel):
    description: str
    context: Optional[str] = None
    compile: bool = True
    generate_docs: bool = True
    board: Optional[str] = "esp32dev"  # uno, nano, esp32dev, default esp32dev

class CodeGenerationResponse(BaseModel):
    description: str
    generated_code: str
    file_path: Optional[str] = None
    success: Optional[bool] = None
    compile_success: Optional[bool] = None
    compilation_status: Optional[str] = None
    compilation_output: Optional[str] = None
    compiler: Optional[str] = None
    compilation_time: Optional[float] = None
    generation_time: Optional[float] = None
    lines_of_code: Optional[int] = None
    compilation_success_rate: Optional[float] = None
    average_quality_score: Optional[float] = None
    memory_efficiency_score: Optional[float] = None
    flash_usage_percent: Optional[float] = None
    ram_usage_percent: Optional[float] = None
    evaluation_summary: Optional[str] = None
    mermaid_code: Optional[str] = None
    mermaid_url: Optional[str] = None
    detected_libraries: Optional[List[str]] = None
    error_summary: Optional[str] = None
    troubleshooting_suggestions: Optional[List[str]] = None
    documentation: Optional[str] = None
    installation_guide: Optional[str] = None
    compilation_error_summary: Optional[str] = None
    compiled_binary_path: Optional[str] = None
    dependency_report: Optional[Dict] = None

    hardware_info: Optional[Dict] = None
    code_quality_score: Optional[int] = None
    memory_usage: Optional[float] = None
    quality_issues: Optional[List[Any]] = None
    quality_warnings: Optional[List[Any]] = None


# 🔥 REQUIRED for Pydantic v2
CodeGenerationResponse.model_rebuild()
