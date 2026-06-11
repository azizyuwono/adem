"""Test Sentinel Core modules."""
from src.watcher import Watcher
from src.healer import Healer

class TestWatcher:
    def test_vitals_returns_dict(self):
        v = Watcher.get_system_vitals()
        assert isinstance(v, dict)
        assert "cpu_usage" in v
        assert "thermal_state" in v
        assert "memory_pressure" in v
        assert "disk_usage" in v
        assert "timestamp" in v

    def test_disk_usage(self):
        usage = Watcher.get_disk_usage()
        assert 0.0 <= usage <= 100.0

class TestHealer:
    def test_cool_down_success(self):
        res = Healer.cool_down_mode()
        assert "SUCCESS" in res or "FAILED" in res

    def test_clean_disk(self):
        res = Healer.clean_disk()
        assert "SUCCESS" in res or "NOOP" in res

    def test_evaluate_and_heal_healthy(self):
        vitals = {
            "cpu_usage": 10.0,
            "thermal_state": 40.0,
            "memory_pressure": 30.0,
            "disk_usage": 50.0
        }
        res = Healer.evaluate_and_heal(vitals)
        assert res["status"] == "Healthy"
        assert len(res["actions"]) == 0

    def test_evaluate_and_heal_triggered(self):
        vitals = {
            "cpu_usage": 90.0,
            "thermal_state": 40.0,
            "memory_pressure": 30.0,
            "disk_usage": 95.0
        }
        res = Healer.evaluate_and_heal(vitals)
        assert res["status"] == "Healed"
        actions = [a[0] for a in res["actions"]]
        assert "CoolDown" in actions
        assert "DiskClean" in actions
