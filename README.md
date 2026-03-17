# oops

oops is a tiny CLI that reruns a failing command, captures the error trace, and asks Gemini for a structured fix suggestion.

## Installation

```bash
pipx install git+https://github.com/ibrahimi46/oops.git
```

Don't have `pipx`?

```bash
brew install pipx
pipx ensurepath
```

## Setup

oops needs your Gemini browser cookies to authenticate. Get them from your browser after logging in to [gemini.google.com](https://gemini.google.com):

1. Open DevTools → Application → Cookies → `https://gemini.google.com`
2. Copy the values of `__Secure-1PSID` and `__Secure-1PSIDTS`

Then run these two commands to add them permanently to your shell (replace the values with yours):

```bash
echo 'export GEMINI_1PSID=your_value_here' >> ~/.zshrc
echo 'export GEMINI_1PSIDTS=your_value_here' >> ~/.zshrc
source ~/.zshrc
```

> Using bash instead of zsh? Replace `~/.zshrc` with `~/.bashrc`.

## Usage

```bash
oops "<your-failed-command>"
```

Examples:

```bash
# React project
oops "npm run dev"

# Python project
oops "python app.py"
```

If the command succeeds, oops prints:

- No Errors Detected!

If the command fails, oops prints:

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
