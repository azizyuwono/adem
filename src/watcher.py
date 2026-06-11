import os
import subprocess
import time
from typing import Dict, Any

class Watcher:
    """Monitors macOS system vitals (Temperature, CPU, RAM, Disk)."""
    
    @staticmethod
    def get_cpu_temp() -> float:
        """Fetch CPU thermal state (nominal/warning/critical mapping to numeric values)."""
        try:
            res = subprocess.check_output(["pmset", "-g", "therm"]).decode()
            if "No thermal warning" in res:
                return 40.0 # Nominal
            return 80.0 # Warning
        except Exception:
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
        except Exception:
            return 0.0

    @staticmethod
    def get_memory_pressure() -> float:
        """Fetch RAM memory pressure from vm_stat / memory_pressure."""
        try:
            # sysctl vm.page_free_wanted or similar, but memory_pressure tool outputs percentage directly on macOS
            res = subprocess.check_output(["memory_pressure"]).decode()
            for line in res.split("\n"):
                if "System-wide memory free percentage:" in line:
                    free_pct = float(line.split(":")[1].replace("%", "").strip())
                    return 100.0 - free_pct
            # Fallback parsing via vm_stat if tool output differs
            return 0.0
        except Exception:
            # Simple fallback using vm_stat
            try:
                vm = subprocess.check_output(["vm_stat"]).decode()
                lines = vm.split("\n")
                page_size = 4096
                free = active = inactive = wired = 0
                for line in lines:
                    if "page size of" in line:
                        page_size = int(line.split("bytes")[0].split("of")[1].strip())
                    elif "Pages free:" in line:
                        free = int(line.split(":")[1].strip().replace(".", ""))
                    elif "Pages active:" in line:
                        active = int(line.split(":")[1].strip().replace(".", ""))
                    elif "Pages inactive:" in line:
                        inactive = int(line.split(":")[1].strip().replace(".", ""))
                    elif "Pages wired down:" in line:
                        wired = int(line.split(":")[1].strip().replace(".", ""))
                total = free + active + inactive + wired
                if total > 0:
                    # Memory pressure is roughly (wired + active) / total * 100
                    return ((wired + active) / total) * 100.0
            except Exception:
                pass
            return 0.0

    @staticmethod
    def get_disk_usage(path: str = "/") -> float:
        """Get disk usage percentage for root volume."""
        try:
            stat = os.statvfs(path)
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            return (used / total) * 100.0
        except Exception:
            return 0.0

    @staticmethod
    def get_system_vitals() -> Dict[str, Any]:
        return {
            "cpu_usage": Watcher.get_cpu_usage(),
            "thermal_state": Watcher.get_cpu_temp(),
            "memory_pressure": Watcher.get_memory_pressure(),
            "disk_usage": Watcher.get_disk_usage(),
            "timestamp": time.time()
        }
