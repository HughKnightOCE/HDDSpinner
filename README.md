# HDDSpinner

Keep a sleepy/aging hard drive from repeatedly spinning up (and ticking) by touching a file at a set interval. I built this after putting up with a dying/ticking HDD that clicked loudly every time it woke from idle. This tool keeps the drive “warm” so it doesn’t keep parking/spinning up.

> ⚠️ Note: This **doesn’t repair a failing drive**. Always back up your data. The goal is to reduce annoying spin-up noise and latency during day-to-day use.

---

## What it does

- Periodically accesses one or two files on the target drive to prevent it from sleeping.
- Very lightweight I/O (tiny create/open or append) to minimise wear.
- Optional access log for visibility.
- Designed for Windows, written in Python.

---

## Quick start

1. Install Python 3.10+  
2. Run the script:
   ```bash
   python HDDSpinnerV2.2.py
   ```
3. Choose/confirm the paths on the **target HDD** (e.g., `E:\keepaliveA.tmp`, `E:\keepaliveB.tmp`) and an interval that suits (e.g., 30–120s).
4. Leave it running while you work. Stop it any time with `Ctrl+C`.

> Tip: Put the keep-alive files on the **drive you want kept awake**.

---

## Build a Windows `.exe` (optional)

If you want a standalone app:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed HDDSpinnerV2.2.py
```

The executable will appear in the `dist/` folder.

---

## Settings (typical)

- **Interval:** 30–120 seconds is usually enough.
- **File paths:** two alternating files on the target drive:
  - `E:\keepaliveA.tmp`
  - `E:\keepaliveB.tmp`
- **Logging:** optional `access_log.txt` for timestamps.

---

## Why I built it

I had a ticking/aging HDD that would spin down aggressively. Every spin-up caused loud clicking and delays when opening files. This small tool keeps the drive active with minimal I/O so the system feels snappy and (most importantly) quiet.

---

## Limitations

- Won’t fix failing hardware; use it only as a convenience.
- Slightly higher idle power usage because the drive stays awake.
- Windows-focused; should run on Linux/macOS but not tested.

---

## License

MIT © Hugh Knight
