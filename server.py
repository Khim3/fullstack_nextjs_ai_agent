import os
import sys
from fastmcp import FastMCP

# Read folder path passed from MCP config
FOLDER = sys.argv[1] if len(sys.argv) > 1 else "."
FOLDER = os.path.abspath(FOLDER)

app = FastMCP()

@app.tool()
def list_files():
    """List all files in the target directory."""
    if not os.path.isdir(FOLDER):
        return {"error": f"{FOLDER} is not a valid directory."}
    print(f"Listing files in directory: {FOLDER}")
    return {
        "path": FOLDER,
        "files": os.listdir(FOLDER)
    }

@app.tool()
def read_file(filename: str):
    """Read the content of a file inside the target directory."""
    filepath = os.path.join(FOLDER, filename)

    if not os.path.exists(filepath):
        return {"error": f"File not found: {filename}"}

    if not os.path.isfile(filepath):
        return {"error": f"Not a file: {filename}"}

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"Read file: {filepath}")
    return {
        "filename": filename,
        "content": content
    }

@app.tool()
def file_exists(filename: str):
    """Check if a file exists."""
    filepath = os.path.join(FOLDER, filename)
    print(f"Checking if file exists: {filepath}")
    return {
        "filename": filename,
        "exists": os.path.exists(filepath)
    }

if __name__ == "__main__":
    print(f"📁 FastMCP server working inside: {FOLDER}")
    app.run()
