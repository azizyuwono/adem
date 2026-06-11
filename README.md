# adem

A lightweight, reactive health monitor for macOS. It watches system vitals and performs targeted clean-up actions when the machine shows signs of thermal or memory pressure.

Built primarily for Intel-based MacBooks that tend to run hot under sustained load.

---

## How It Works

Adem runs as a simple polling loop. Each cycle:

1. **Watcher** reads current CPU load, thermal state, memory pressure, and disk usage through macOS built-in tools (`pmset`, `top`, `vm_stat`, `memory_pressure`).
2. **Healer** evaluates the readings against defined thresholds.
3. If any threshold is crossed, Adem executes a response:
   - **CPU/Thermal**: Requests a system memory purge to reduce swap-related CPU overhead.
   - **Memory**: Triggers memory cleanup.
   - **Disk**: Cleans up development caches (pip, brew, npm, yarn) if usage > 90%.

No daemon, no background agent. It is designed to be triggered externally — by a cron job, a CI runner, or by hand when the fans feel loud.

## Project Structure

```
src/
├── watcher.py   # Reads system vitals
├── healer.py    # Decides and executes responses
└── main.py      # CLI entry point

tests/
└── test_core.py # Unit tests

logs/            # Health records and logs
```

## Local Development

```bash
git clone git@github.com:azizyuwono/adem.git
cd adem
pip install -r requirements.txt
PYTHONPATH=. python3 -m pytest tests/
python3 src/main.py
```

## Running on a Schedule

Add to crontab to run every 30 minutes:
```bash
*/30 * * * * cd /path/to/adem && /usr/bin/python3 src/main.py
```

---

*Maintained by [Moli](https://t.me/davevy).*
