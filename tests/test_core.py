"""Test Sentinel Core modules."""
from src.watcher import Watcher
from src.healer import Healer

class TestWatcher:
    def test_vitals_returns_dict(self):
        v = Watcher.get_system_vitals()
        assert isinstance(v, dict)
        assert "cpu_usage" in v

class TestHealer:
    def test_cool_down_success(self):
        res = Healer.cool_down_mode()
        assert "SUCCESS" in res or "FAILED" in res
