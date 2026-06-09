# adem

A lightweight, reactive health monitor for macOS. It watches system vitals and performs targeted clean-up actions when the machine shows signs of thermal or memory pressure.

Built primarily for Intel-based MacBooks that tend to run hot under sustained load.

---

## How It Works

Adem runs as a simple polling loop. Each cycle:

1. **Watcher** reads current CPU load, thermal state, and memory pressure through macOS built-in tools (`pmset`, `top`, `vm_stat`).
2. **Healer** evaluates the readings against defined thresholds.
3. If any threshold is crossed, Adem executes a response — typically a memory purge or a log entry for later review.

No daemon, no background agent. It is designed to be triggered externally — by a cron job, a CI runner, or by hand when the fans feel loud.

## Project Structure

```
src/
├── watcher.py   # Reads system vitals
├── healer.py    # Decides and executes responses
└── main.py      # Single-run entry point

tests/
└── test_core.py # Verifies module contracts

.github/workflows/
└── daily.yml    # Scheduled daily run via GitHub Actions

logs/            # Output directory for health records
```

## Local Development

```bash
git clone git@github.com:azizyuwono/adem.git
cd adem
pip install -r requirements.txt
python -m pytest tests/
python -m src.main
```

## Running on a Schedule

Adem can be added to a local cron job (e.g. every 30 minutes) or run manually when the system feels sluggish. It outputs plain text logs that can be consumed by other tools or simply inspected at the end of the day.

## Motivation

Most system monitoring tools either require a full dashboard setup or run as heavy background services. Adem takes the opposite approach: it is small, stateless, and does nothing unless something is wrong. It exists to be *called*, not to run.

---

*Maintained by [Moli](https://t.me/davevy).*
