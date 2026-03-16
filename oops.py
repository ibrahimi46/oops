import subprocess
import os
import sys
import asyncio
from gemini_webapi import GeminiClient
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


psid = os.getenv("GEMINI_1PSID")
psidts = os.getenv("GEMINI_1PSIDTS")

console = Console()

def capture_error(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    error_output = result.stderr if result.stderr.strip() else result.stdout

    return result.returncode, error_output


async def get_gemini_fix(error_message):
    client = GeminiClient(psid, psidts)
    await client.init(timeout=30, auto_refresh=True)
    prompt = (
    "You are a senior developer. Analyze this terminal error trace. "
    "Strictly follow this format for your response and do not print anything besides these:\n\n"
    "file: [Path to the file that caused the error]\n"
    "error: [A short, one-sentence explanation of what went wrong]\n"
    "fix: [The exact code snippet or command to fix the issue]\n\n"
    f"Error Trace:\n{error_message}"
)


    response = await client.generate_content(prompt=prompt)
    return response.text


async def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Usage:[/bold red] oops <last_command>")        
        sys.exit(1)

    last_error = sys.argv[1]

    exit_code, error_output = capture_error(last_error)

    if exit_code == 0:
        console.print("[bold green]No Errors Detected! [/bold green]")
        return

    with console.status("[bold cyan]Asking Gemini for a fix...", spinner="dots"):
        gemini_fix = await get_gemini_fix(error_message=error_output)
        lines = [line.strip() for line in gemini_fix.split("\n") if line.strip()]

        file_info = lines[0]
        error_info = lines[1]
        suggested_fix = lines[2]


    console.print(Panel(f"[bold red]Error in:[/bold red] {file_info}\n[bold yellow]Description:[/bold yellow] {error_info}", title="Analysis", border_style="red"))
    syntax = Syntax(suggested_fix, "python", theme="monokai")
    console.print(Panel(syntax, title="Suggested Fix", border_style="green"))
        

    

if __name__ == "__main__":
    asyncio.run(main())
