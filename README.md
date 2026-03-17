# oops

Oops is a tiny CLI that reruns a failing command, captures the error trace, and asks Gemini for a structured fix suggestion.

## Demo

[Watch Demo Video](https://your-demo-link-here)

![Demo Placeholder](https://placehold.co/1200x700/111827/E5E7EB?text=Oops+CLI+Demo)

## Why Oops

- Fast feedback when a command fails
- Clean terminal output with focused analysis
- Structured response: file, error, and fix

## Quick Start

1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies
4. Add your Gemini cookies to a .env file

Example:

```bash
git clone <your-repo-url>
cd oops
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_1PSID=your_value_here
GEMINI_1PSIDTS=your_value_here
```

Run:

```bash
python3 oops.py "python3 -c 'print(1/0)'"
```

## Usage

```bash
python3 oops.py "<your-failed-command>"
```

If the command succeeds, Oops prints:

- No Errors Detected!

If the command fails, Oops prints:

- Analysis panel (error file and short description)
- Suggested Fix panel (actionable fix snippet/command)

## How It Works

1. Executes your command
2. Captures stderr/stdout if it fails
3. Sends command + trace to Gemini with a strict JSON prompt
4. Parses response into:
   - file
   - error
   - fix
5. Displays result in Rich panels

## Credit

This project uses the excellent Gemini WebAPI library:

- https://github.com/HanaokaYuzu/Gemini-API

Big thanks to the maintainers and contributors.

## Notes

- AI output can be wrong. Always review fixes before applying.
- Keep your .env private and never commit cookie values.
