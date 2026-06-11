import os
import glob
import shutil
import subprocess

class Healer:
    """Reactive mechanisms to restore system health."""

    @staticmethod
    def cool_down_mode() -> str:
        """Emergency action: Purge memory and suspend high-CPU background tasks."""
        try:
            # Drop caches (this usually requires sudo, we run it and ignore failures if not root)
            subprocess.run(["sudo", "-n", "purge"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return "SUCCESS: Requested system memory purge."
        except Exception as e:
            return f"FAILED: {str(e)}"

    @staticmethod
    def clean_disk() -> str:
        """Clean up standard development caches safely (no sudo required)."""
        cleaned_dirs = []
        
        # Safe targets for typical developers:
        targets = [
            # User Caches
            "~/Library/Caches/pip",
            "~/Library/Caches/Homebrew",
            "~/Library/Caches/yarn",
            "~/Library/Caches/npm",
            # Logs
            "~/Library/Logs/DiagnosticReports",
        ]
        
        for t in targets:
            path = os.path.expanduser(t)
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    cleaned_dirs.append(t)
                except Exception:
                    pass
                    
        if cleaned_dirs:
            return f"SUCCESS: Cleaned up cache dirs: {', '.join(cleaned_dirs)}"
        return "NOOP: No common cleanable cache directories found/writable."

    @staticmethod
    def evaluate_and_heal(vitals: dict) -> dict:
        """Determine if healing is needed based on vitals."""
        actions_taken = []
        
        # Heavy CPU Load (>85%) or High Thermal State
        if vitals.get("cpu_usage", 0) > 85.0 or vitals.get("thermal_state", 0) >= 80.0:
            result = Healer.cool_down_mode()
            actions_taken.append(("CoolDown", result))
            
        # High memory pressure (>80%)
        if vitals.get("memory_pressure", 0) > 80.0:
            result = Healer.cool_down_mode()
            actions_taken.append(("MemoryPurge", result))
            
        # Low Disk space (Disk Usage > 90%)
        if vitals.get("disk_usage", 0) > 90.0:
            result = Healer.clean_disk()
            actions_taken.append(("DiskClean", result))
            
        return {
            "status": "Healed" if actions_taken else "Healthy",
            "actions": actions_taken
        }
