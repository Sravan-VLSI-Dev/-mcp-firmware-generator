from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()
ARDUINO_CLI = r"D:\\MCP\\arduino-cli.exe"
class CompileRequest(BaseModel):
    code: str
    board: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/compile")
def compile_code(request: CompileRequest):

    board = request.board

    # Create temporary sketch directory
    with tempfile.TemporaryDirectory() as sketch_dir:

        sketch_folder_name = os.path.basename(sketch_dir)
        sketch_path = os.path.join(sketch_dir, f"{sketch_folder_name}.ino")

        # Write code to file
        with open(sketch_path, "w") as f:
            f.write(request.code)

        try:
            result = subprocess.run(
                [
                    ARDUINO_CLI,
                    "compile",
                    "--fqbn",
                    board,
                    sketch_dir
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}

        except Exception as e:
            return {"success": False, "error": str(e)}
