#!/usr/bin/env python3
import os
import sys
import json
import logging
from datetime import datetime, timezone

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from watcher import Watcher
from healer import Healer

# Setup logs dir
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, "adem.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    logging.info("Starting adem health check run")
    try:
        vitals = Watcher.get_system_vitals()
        logging.info(f"Vitals: {json.dumps(vitals)}")
        
        healing_result = Healer.evaluate_and_heal(vitals)
        
        if healing_result["status"] == "Healed":
            logging.warning(f"Healing actions executed: {healing_result['actions']}")
        else:
            logging.info("System healthy, no actions needed.")
            
        # Write report run record
        report_path = os.path.join(LOGS_DIR, "report_latest.json")
        with open(report_path, "w") as f:
            json.dump({
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "vitals": vitals,
                "healing": healing_result
            }, f, indent=2)
            
        logging.info("Run finished successfully.")
    except Exception as e:
        logging.error(f"Error in adem run loop: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
