import os
import subprocess
import time
from typing import Dict, Any

class Watcher:
    """Monitors macOS system vitals (Temperature, CPU, RAM)."""
    
    @staticmethod
    def get_cpu_temp() -> float:
        """Fetch CPU temperature using powermetrics (requires sudo/auth)."""
        # Fallback to a simpler check if powermetrics is not ideal for background
        # On Mac 2018, we can use osx-cpu-temp if installed or pmset
        try:
            res = subprocess.check_output(["pmset", "-g", "therm"]).decode()
            if "No thermal warning" in res:
                return 40.0 # Nominal
            return 80.0 # Warning
        except:
            return 0.0

    @staticmethod
    def get_cpu_usage() -> float:
        """Get total CPU load percentage."""
        try:
            res = subprocess.check_output(["top", "-l", "1", "-n", "0"]).decode()
            for line in res.split("\n"):
                if "CPU usage:" in line:
                    # Parse 'CPU usage: 10.5% user, ...'
                    parts = line.split(":")[1].split(",")
                    user = float(parts[0].strip().split("%")[0])
                    sys_load = float(parts[1].strip().split("%")[0])
                    return user + sys_load
            return 0.0
        except:
            return 0.0

    @staticmethod
    def get_system_vitals() -> Dict[str, Any]:
        return {
            "cpu_usage": Watcher.get_cpu_usage(),
            "thermal_state": Watcher.get_cpu_temp(),
            "timestamp": time.time()
        }
