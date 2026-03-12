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
        "You are a helpful coding assistant. I got an error in my terminal. "
        "Please identify the file, explain the error briefly, and provide a fix.\n\n"
        f"Error:\n{error_message}"
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
