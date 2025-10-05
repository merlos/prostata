import pytest
import time
from prostata import Stats
from prostata.Stats import NameNotAllowed, NameExists, NameNotExists


class TestStats:

    def test_init(self):
        stats = Stats()
        assert stats._timers == {}
        assert stats._counters == {}
        assert stats._ratios == {}
        assert stats._attributes == {}
        assert stats._names_used == set()

    def test_is_used(self):
        stats = Stats()
        assert not stats.is_used("test")
        stats.set_counter("test")
        assert stats.is_used("test")

    def test_set_timer(self):
        stats = Stats()
        stats.set_timer("my_timer")
        assert "my_timer" in stats._timers
        assert stats._timers["my_timer"] == {'start': None, 'stop': None, 'segments': 0, 'elapsed': 0.0}
        assert "my_timer" in stats._names_used

    def test_set_timer_forbidden_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_timer("timer")

    def test_set_timer_existing_name(self):
        stats = Stats()
        stats.set_counter("test")
        with pytest.raises(NameExists):
            stats.set_timer("test")

    def test_set_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", 10, "units")
        assert "my_counter" in stats._counters
        assert stats._counters["my_counter"] == {'value': 10, 'unit': "units"}

    def test_set_counter_defaults(self):
        stats = Stats()
        stats.set_counter("my_counter")
        assert stats._counters["my_counter"] == {'value': 0, 'unit': "item"}

    def test_set_ratio(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("my_ratio", "num", "den")
        assert "my_ratio" in stats._ratios
        assert stats._ratios["my_ratio"] == {'numerator': "num", 'denominator': "den", 'value': 0.0}

    def test_set_ratio_nonexistent_num(self):
        stats = Stats()
        stats.set_counter("den")
        with pytest.raises(NameNotExists):
            stats.set_ratio("my_ratio", "num", "den")

    def test_set_ratio_nonexistent_den(self):
        stats = Stats()
        stats.set_counter("num")
        with pytest.raises(NameNotExists):
            stats.set_ratio("my_ratio", "num", "den")

    def test_set_attribute(self):
        stats = Stats()
        stats.set_attribute("my_attr", "value")
        assert stats._attributes["my_attr"] == "value"

    def test_set_attribute_types(self):
        stats = Stats()
        stats.set_attribute("str_attr", "string")
        stats.set_attribute("int_attr", 42)
        stats.set_attribute("float_attr", 3.14)
        assert stats._attributes["str_attr"] == "string"
        assert stats._attributes["int_attr"] == 42
        assert stats._attributes["float_attr"] == 3.14

    def test_get_timer_not_started(self):
        stats = Stats()
        stats.set_timer("my_timer")
        assert stats.get_timer("my_timer") == 0.0

    def test_get_timer_started(self):
        stats = Stats()
        stats.set_timer("my_timer")
        stats.start_timer("my_timer")
        time.sleep(0.01)  # small delay
        elapsed = stats.get_timer("my_timer")
        assert elapsed > 0

    def test_get_timer_stopped(self):
        stats = Stats()
        stats.set_timer("my_timer")
        stats.start_timer("my_timer")
        time.sleep(0.01)
        stats.stop_timer("my_timer")
        elapsed = stats.get_timer("my_timer")
        assert elapsed > 0
        # After stop, should not increase
        time.sleep(0.01)
        assert stats.get_timer("my_timer") == elapsed

    def test_start_stop_timer(self):
        stats = Stats()
        stats.set_timer("my_timer")
        stats.start_timer("my_timer")
        assert stats._timers["my_timer"]["start"] is not None
        stats.stop_timer("my_timer")
        assert stats._timers["my_timer"]["start"] is None
        assert stats._timers["my_timer"]["stop"] is not None

    def test_get_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", 5)
        assert stats.get_counter("my_counter") == 5

    def test_incr_decr_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", 10)
        stats.incr("my_counter", 5)
        assert stats.get_counter("my_counter") == 15
        stats.decr("my_counter", 3)
        assert stats.get_counter("my_counter") == 12

    def test_reset_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", 10)
        stats.reset_counter("my_counter", 0)
        assert stats.get_counter("my_counter") == 0

    def test_set_counter_unit(self):
        stats = Stats()
        stats.set_counter("my_counter")
        stats.set_counter_unit("my_counter", "bytes")
        assert stats._counters["my_counter"]["unit"] == "bytes"

    def test_get_ratio(self):
        stats = Stats()
        stats.set_counter("num", 10)
        stats.set_counter("den", 2)
        stats.set_ratio("my_ratio", "num", "den")
        assert stats.get_ratio("my_ratio") == 5.0

    def test_get_ratio_zero_denominator(self):
        stats = Stats()
        stats.set_counter("num", 10)
        stats.set_counter("den", 0)
        stats.set_ratio("my_ratio", "num", "den")
        assert stats.get_ratio("my_ratio") == 0.0

    def test_get_attribute(self):
        stats = Stats()
        stats.set_attribute("my_attr", "test")
        assert stats.get_attribute("my_attr") == "test"

    def test_set_attribute_value(self):
        stats = Stats()
        stats.set_attribute("my_attr", "initial")
        stats.set_attribute_value("my_attr", "updated")
        assert stats.get_attribute("my_attr") == "updated"

    def test_dynamic_methods(self):
        stats = Stats()
        stats.set_timer("timer1")
        stats.set_counter("counter1")
        stats.set_ratio("ratio1", "counter1", "counter1")  # ratio of counter to itself
        stats.set_attribute("attr1", "value")

        # Test dynamic gets
        assert hasattr(stats, "get_timer1")
        assert hasattr(stats, "get_counter1")
        assert hasattr(stats, "get_ratio1")
        assert hasattr(stats, "get_attr1")

        # Test dynamic sets
        assert hasattr(stats, "start_timer1")
        assert hasattr(stats, "stop_timer1")
        assert hasattr(stats, "incr_counter1")
        assert hasattr(stats, "decr_counter1")
        assert hasattr(stats, "reset_counter1")
        assert hasattr(stats, "set_attr1")

    def test_exceptions_on_nonexistent(self):
        stats = Stats()
        with pytest.raises(NameNotExists):
            stats.get_timer("nonexistent")
        with pytest.raises(NameNotExists):
            stats.start_timer("nonexistent")
        with pytest.raises(NameNotExists):
            stats.stop_timer("nonexistent")
        with pytest.raises(NameNotExists):
            stats.get_counter("nonexistent")
        with pytest.raises(NameNotExists):
            stats.incr("nonexistent")
        with pytest.raises(NameNotExists):
            stats.decr("nonexistent")
        with pytest.raises(NameNotExists):
            stats.reset_counter("nonexistent")
        with pytest.raises(NameNotExists):
            stats.set_counter_unit("nonexistent", "unit")
        with pytest.raises(NameNotExists):
            stats.get_ratio("nonexistent")
        with pytest.raises(NameNotExists):
            stats.get_attribute("nonexistent")
        with pytest.raises(NameNotExists):
            stats.set_attribute_value("nonexistent", "value")