# Sentinel Core

Autonomous system diagnostic and self‑healing engine for macOS.

Born from the frustration of an aging MacBook Intel that throttles
under load and runs hot even when idling.

## How It Lives

- `Watcher` polls CPU temperature, load, memory pressure, and
  other vitals through the system's own metrics (no third‑party
  kernel extensions).
- `Healer` decides what to do when things go wrong — emit a last‑resort
  purge, nudge runaway processes, or just record the event for
  later analysis.

## Design

The engine is kept minimal on purpose. No daemon, no launchd plist.
It exists to be *called* — manually, by a cron job, or by another
system agent (like a Hermes profile). Complexity is avoided; clarity
is preferred.

```bash
python -m src.main
```

## Tests

```bash
pip install -r requirements.txt
pytest
```