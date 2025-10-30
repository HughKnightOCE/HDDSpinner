# HDDSpinner

Keep a sleepy/aging hard drive from repeatedly spinning up (and ticking) by touching a file at a set interval.

I built this after putting up with a dying/ticking HDD That clicked loudly every time it woke from idle. This tool keeps the drive ‚warm’ so it doesn’t keep parking/spinning up.

> ₭ — This doesn’t repair a failing drive. Always back up your data.

# Quick start
```bash
python src/HDDSpinnerV2.2.py
```
When prompted, choose two keep-alive file paths on the drive you want to keep awake (e.g., E\:keepaliveA.tmp, E\kiepaliveB.tmp) and pick an interval (30–120s's works well).

# Build a Windows .exe (optional)
```bash
pip install pyinstaller
py