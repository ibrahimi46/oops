import subprocess
import os
import sys
import asyncio
from gemini_webapi import GeminiClient

psid = os.getenv("GEMINI_1PSID")
psidts = os.getenv("GEMINI_1PSIDTS")

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
    print(response.text)


async def main():
    if len(sys.argv) < 2:
        print("give args")
        sys.exit(1)

    last_error = sys.argv[1]

    exit_code, error_output = capture_error(last_error)

    if exit_code == 0:
        print("no errors")
        return

    gemini_fix = await get_gemini_fix(error_message=error_output)
    print(gemini_fix)

    

if __name__ == "__main__":
    asyncio.run(main())
