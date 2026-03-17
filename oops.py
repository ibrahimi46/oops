import subprocess
import os
import sys
import asyncio
import re
from gemini_webapi import GeminiClient
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import json


psid = os.getenv("GEMINI_1PSID")
psidts = os.getenv("GEMINI_1PSIDTS")

console = Console()

def capture_error(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    error_output = result.stderr if result.stderr.strip() else result.stdout

    return result.returncode, error_output


def parse_gemini_response(text):
    raw = text.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json\n", "", 1).strip()

    start = raw.find("{")
    end = raw.rfind("}")
    candidate = raw[start : end + 1] if start != -1 and end != -1 and end > start else raw

    # Remove invalid escapes like \< or \> that break json.loads.
    candidate = re.sub(r"\\([^\"\\/bfnrtu])", r"\1", candidate)

    try:
        data = json.loads(candidate)
        if not all(k in data for k in ("file", "error", "fix")):
            raise ValueError("Missing required keys")
        
        return {
            "file": str(data["file"]).strip() or "unknown",
            "error": str(data["error"]).strip() or "No error summary provided",
            "fix": str(data["fix"]).strip() or "No fix provided",
        }
    except Exception:
        return {
            "file": "unknown",
            "error": "Could not parse Gemini response",
            "fix": raw or "No fix returned",
        }      

async def get_gemini_fix(command, error_message):
    client = GeminiClient(psid, psidts)
    await client.init(timeout=30, auto_refresh=True, verbose=False)
    prompt = (
        "You are a senior debugging assistant.\n\n"
        "You must analyze only the provided command and terminal error trace.\n"
        "Do not guess missing details.\n"
        "Do not invent files, stack frames, modules, or project structure.\n\n"
        f"Failed command:\n{command}\n\n"
        f"Terminal error trace:\n{error_message}\n\n"
        "Return only one valid JSON object with exactly these keys and no others:\n"
        "{\n"
        '  "file": "string",\n'
        '  "error": "string",\n'
        '  "fix": "string"\n'
        "}\n\n"
        "Rules:\n"
        "1. file:\n"
        "- If an explicit file path appears in the trace, use that exact path.\n"
        "- If no explicit file path appears, return \"unknown\".\n\n"
        "2. error:\n"
        "- One short sentence describing the real root cause from the trace only.\n"
        "- No generic advice.\n\n"
        "3. fix:\n"
        "- Provide a concrete, minimal fix command or code snippet tied to this specific error.\n"
        "- If confidence is low, still provide the safest next actionable step.\n\n"
        "Output constraints:\n"
        "- Output raw JSON only.\n"
        "- No markdown.\n"
        "- No code fences.\n"
        "- No extra commentary before or after JSON."
    )


    response = await client.generate_content(prompt=prompt)
    return response.text


async def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] oops <last_command>")        
        sys.exit(1)

    last_command = sys.argv[1]
    
    exit_code, error_output = capture_error(last_command)

    if exit_code == 0:
        console.print("[bold green]No Errors Detected! [/bold green]")
        return

    with console.status("[bold cyan]Asking Gemini for a fix...", spinner="dots"):
        gemini_fix = await get_gemini_fix(command=last_command, error_message=error_output)
        parsed = parse_gemini_response(gemini_fix)

        file_info = parsed["file"]
        error_info = parsed["error"]
        suggested_fix = parsed["fix"]


    console.print(Panel(f"[bold red]Error in:[/bold red] {file_info}\n[bold yellow]Description:[/bold yellow] {error_info}", title="Analysis", border_style="red"))
    syntax = Syntax(suggested_fix, "python", theme="monokai")
    console.print(Panel(syntax, title="Suggested Fix", border_style="green"))
        

    

if __name__ == "__main__":
    asyncio.run(main())
