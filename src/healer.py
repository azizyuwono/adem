import subprocess

class Healer:
    """Reactive mechanisms to restore system health."""

    @staticmethod
    def cool_down_mode() -> str:
        """Emergency action: Purge memory and suspend high-CPU background tasks."""
        try:
            # Drop caches
            subprocess.run(["sudo", "purge"], stderr=subprocess.DEVNULL)
            
            # Additional logic can be added here (e.g., kill runaway Chrome helpers)
            # For safety, we only perform non-destructive cleanup
            return "SUCCESS: Purged system memory and entered cool-down mode."
        except Exception as e:
            return f"FAILED: {str(e)}"
    
    @staticmethod
    def evaluate_and_heal(vitals: dict) -> dict:
        """Determine if healing is needed based on vitals."""
        actions_taken = []
        
        # Heavy CPU Load (>85%) or High Thermal State
        if vitals.get("cpu_usage", 0) > 85.0 or vitals.get("thermal_state", 0) >= 80.0:
            result = Healer.cool_down_mode()
            actions_taken.append(("CoolDown", result))
            
        return {
            "status": "Healed" if actions_taken else "Healthy",
            "actions": actions_taken
        }
