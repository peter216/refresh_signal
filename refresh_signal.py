import os
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

# Determine Blink(1) CLI path:
# - If `BLINK1_TOOL` env var is set, use it
# - Else try a reasonable default under the user's profile
# - Else fall back to `blink1-tool.exe` (assumes it's on PATH)
BLINK1_TOOL_ENV = os.environ.get("BLINK1_TOOL")
if BLINK1_TOOL_ENV:
    BLINK1 = BLINK1_TOOL_ENV
else:
    user_profile = os.environ.get("USERPROFILE") or str(Path.home())
    default_blink1 = (
        Path(user_profile)
        / "Program_Files"
        / "blink1-tool-v2.5.0-windows-x86_64"
        / "blink1-tool.exe"
    )
    if default_blink1.exists():
        BLINK1 = str(default_blink1)
    else:
        BLINK1 = "blink1-tool.exe"

# Reminder page: allow override with BREAK_REMINDER_PAGE env var, otherwise use script-relative file
REMINDER_PAGE = os.environ.get("BREAK_REMINDER_PAGE") or str(
    Path(__file__).resolve().parent / "break_reminder.html"
)

hour = datetime.now().hour

LOG_FILE = Path(__file__).resolve().parent / "refresh_signal.log"


def _log(msg: str):
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


_log(
    f"START user={os.environ.get('USERNAME')} userprofile={os.environ.get('USERPROFILE')} BLINK1={BLINK1} REMINDER_PAGE={REMINDER_PAGE}"
)

cmd = [BLINK1, "--green" if hour % 2 == 0 else "--yellow", "--flash", "3"]
_log(f"Running LED command: {cmd}")
try:
    cp = subprocess.run(cmd, capture_output=True, text=True)
    _log(
        f"LED exit={cp.returncode} stdout={cp.stdout.strip()!r} stderr={cp.stderr.strip()!r}"
    )
except FileNotFoundError as e:
    _log(f"LED FileNotFoundError: {e}")
except Exception as e:
    _log(f"LED Exception: {type(e).__name__}: {e}")

# Open the reminder page — auto-scrolls to the right section based on hour parity
_log(f"Opening reminder page: {REMINDER_PAGE}")
try:
    opened = webbrowser.open(Path(REMINDER_PAGE).as_uri())
    _log(f"webbrowser.open returned: {opened}")
except Exception as e:
    _log(f"webbrowser.open Exception: {type(e).__name__}: {e}")

_log("END")
