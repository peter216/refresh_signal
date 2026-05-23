Blink(1) Break Signal — Scripts
===============================

What this does
--------------

A tiny set of Windows scripts that drive a Blink(1) USB RGB notification light and show a local "take a break" web page.

- On even hours the Blink(1) flashes green 3× and the page jumps to the "Green / Body Reset" panel.
- On odd hours the Blink(1) flashes yellow 3× and the page jumps to the "Yellow / Mind Reset" panel.

Files
-----

- `refresh_signal.py` — Main Python script. Calls the Blink(1) command-line tool to flash the light and opens `break_reminder.html` in your default browser.
- `break_reminder.html` — Local reminder page with two themed panels (green / yellow) and an auto-scroll that selects the correct panel based on hour parity.
- `run_hidden.vbs` — Lightweight Windows VBScript wrapper to launch `refresh_signal.py` hidden (no console window).

How it works
------------

`refresh_signal.py` checks the current hour. If `hour % 2 == 0` it runs the Blink(1) CLI with the `--green --flash 3` arguments; otherwise it runs `--yellow --flash 3`. After firing the LED sequence it opens the `break_reminder.html` file in the default browser. The VBScript `run_hidden.vbs` runs the Python script invisibly.

Configuration
-------------

This repository now supports environment-based configuration so you don't need to hard-code your username or machine-specific paths.

Environment variables (optional)
--------------------------------

- `BLINK1_TOOL` — full path to the Blink(1) CLI executable. If set, `refresh_signal.py` will use this value.
- `BREAK_REMINDER_PAGE` — full path to the `break_reminder.html` file to open (useful if you move the HTML somewhere else).
- `PYTHON_EXE` — used by `run_hidden.vbs` to choose a specific Python executable; if not set, the script uses `python` from PATH.

Behavior if env vars are not set
--------------------------------

- `refresh_signal.py` falls back to a reasonable default under the current user's profile (derived from `%USERPROFILE%` / `Path.home()`), and finally to `blink1-tool.exe` on the PATH if no executable is found.
- `run_hidden.vbs` expands `%USERPROFILE%` to locate `refresh_signal.py` and will use `python` from the PATH unless `PYTHON_EXE` is set.

Running
-------

Quick test (PowerShell) — set env vars for this session and run:

```powershell
$env:BLINK1_TOOL = 'C:\path\to\blink1-tool.exe'
$env:BREAK_REMINDER_PAGE = 'C:\path\to\break_reminder.html'
python "C:\Users\$env:USERNAME\Program_Files\Blink1Control2-2.3.0-win-x64\scripts\refresh_signal.py"
```

Run hidden (no console): double-click `run_hidden.vbs` or schedule that VBScript. If you want the scheduled task to work for any user profile, prefer setting `BLINK1_TOOL` and/or `PYTHON_EXE` as permanent user/system environment variables (see Scheduling).

Scheduling
----------

Recommended approaches to make scheduling robust across accounts:

1) Persist the variables as user or system environment variables so Task Scheduler sees them without wrapping the action. From an elevated command prompt you can use `setx` (note `setx` persists the variable for future processes):

```powershell
setx BLINK1_TOOL "C:\path\to\blink1-tool.exe"
setx PYTHON_EXE  "C:\Python311\python.exe"
```

After `setx` the new variables will apply to newly-launched processes (log out/in may be required for system-wide changes).

2) Or schedule a wrapper that sets variables just for that run. Example `schtasks` that runs a one-line `cmd` wrapper which sets env vars and launches the VBScript (note the quoting):

```powershell
schtasks /Create /SC HOURLY /MO 1 /TN "Blink1 Break Signal" /TR "cmd /c \"set BLINK1_TOOL=C:\\path\\to\\blink1-tool.exe && set PYTHON_EXE=C:\\Python311\\python.exe && wscript \"%USERPROFILE%\\Program_Files\\Blink1Control2-2.3.0-win-x64\\scripts\\run_hidden.vbs\"\""
```

3) Simpler: if `BLINK1_TOOL` and/or `PYTHON_EXE` are set with `setx` or in System Properties → Environment Variables, schedule `run_hidden.vbs` directly and the task will use those variables when executed under the same account.

Notes & tips
------------

- Do not check secrets or device drivers into source control. The Blink(1) CLI must be compatible with your device and OS.
- If the LED doesn't flash, verify the `BLINK1_TOOL` path (or the resolved default) in `refresh_signal.py` and test the CLI manually from a command prompt.
- Edit `break_reminder.html` to change the text, tasks, or styling shown during the reminders.

License
-------

MIT — see [LICENSE](LICENSE).

Contact / Changes
-----------------

If you want changes (different colors, timing, or alternate notification behavior), tell me what you'd like and I can update the scripts.
