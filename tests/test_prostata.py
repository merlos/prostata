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
        assert stats._timers["my_timer"] == {'start': None, 'stop': None, 'segments': 0, 'elapsed': 0.0, 'label': 'my_timer'}
        assert "my_timer" in stats._names_used

    def test_set_timer_with_label(self):
        stats = Stats()
        stats.set_timer("my_timer", "My Timer")
        assert "my_timer" in stats._timers
        assert stats._timers["my_timer"]['label'] == 'My Timer'

    def test_set_timer_forbidden_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_timer("timer")
        with pytest.raises(NameNotAllowed):
            stats.set_timer("timers")

    def test_set_timer_invalid_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_timer("Timer")
        with pytest.raises(NameNotAllowed):
            stats.set_timer("my-timer")
        with pytest.raises(NameNotAllowed):
            stats.set_timer("my timer")
        with pytest.raises(NameNotAllowed):
            stats.set_timer("my@timer")

    def test_set_timer_existing_name(self):
        stats = Stats()
        stats.set_counter("test")
        with pytest.raises(NameExists):
            stats.set_timer("test")

    def test_set_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", 10, "units")
        assert "my_counter" in stats._counters
        assert stats._counters["my_counter"] == {'value': 10, 'unit': "units", 'label': 'my_counter'}

    def test_set_counter_defaults(self):
        stats = Stats()
        stats.set_counter("my_counter")
        assert stats._counters["my_counter"] == {'value': 0, 'unit': "item", 'label': 'my_counter'}

    def test_set_counter_with_label(self):
        stats = Stats()
        stats.set_counter("my_counter", 5, "bytes", "My Counter")
        assert stats._counters["my_counter"]['label'] == 'My Counter'

    def test_set_counter_forbidden_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_counter("counter")
        with pytest.raises(NameNotAllowed):
            stats.set_counter("counters")

    def test_set_counter_invalid_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_counter("Counter")
        with pytest.raises(NameNotAllowed):
            stats.set_counter("my-counter")
        with pytest.raises(NameNotAllowed):
            stats.set_counter("my counter")

    def test_set_ratio(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("my_ratio", "num", "den")
        assert "my_ratio" in stats._ratios
        assert stats._ratios["my_ratio"] == {'numerator': "num", 'denominator': "den", 'value': 0.0, 'label': 'my_ratio'}

    def test_set_ratio_with_label(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("my_ratio", "num", "den", "My Ratio")
        assert stats._ratios["my_ratio"]['label'] == 'My Ratio'

    def test_set_ratio_forbidden_name(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        with pytest.raises(NameNotAllowed):
            stats.set_ratio("ratio", "num", "den")
        with pytest.raises(NameNotAllowed):
            stats.set_ratio("ratios", "num", "den")

    def test_set_ratio_invalid_name(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        with pytest.raises(NameNotAllowed):
            stats.set_ratio("Ratio", "num", "den")
        with pytest.raises(NameNotAllowed):
            stats.set_ratio("my-ratio", "num", "den")

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
        assert stats._attributes["my_attr"] == {'value': 'value', 'label': 'my_attr'}

    def test_set_attribute_types(self):
        stats = Stats()
        stats.set_attribute("str_attr", "string")
        stats.set_attribute("int_attr", 42)
        stats.set_attribute("float_attr", 3.14)
        assert stats._attributes["str_attr"]['value'] == "string"
        assert stats._attributes["int_attr"]['value'] == 42
        assert stats._attributes["float_attr"]['value'] == 3.14

    
    def test_set_attribute_forbidden_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_attribute("attribute", "value")
        with pytest.raises(NameNotAllowed):
            stats.set_attribute("attributes", "value")

    def test_set_attribute_invalid_name(self):
        stats = Stats()
        with pytest.raises(NameNotAllowed):
            stats.set_attribute("Attribute", "value")
        with pytest.raises(NameNotAllowed):
            stats.set_attribute("my-attribute", "value")

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

    def test_get_timers(self):
        stats = Stats()
        stats.set_timer("timer1")
        stats.set_timer("timer2")
        timers = stats.get_timers()
        assert "timer1" in timers
        assert "timer2" in timers
        assert len(timers) == 2

    def test_get_counters(self):
        stats = Stats()
        stats.set_counter("counter1", 10)
        stats.set_counter("counter2", 20)
        counters = stats.get_counters()
        assert "counter1" in counters
        assert "counter2" in counters
        assert counters["counter1"]["value"] == 10
        assert counters["counter2"]["value"] == 20

    def test_get_ratios(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("ratio1", "num", "den")
        ratios = stats.get_ratios()
        assert "ratio1" in ratios
        assert ratios["ratio1"]["numerator"] == "num"
        assert ratios["ratio1"]["denominator"] == "den"

    def test_get_attributes(self):
        stats = Stats()
        stats.set_attribute("attr1", "value1")
        stats.set_attribute("attr2", 42)
        attributes = stats.get_attributes()
        assert "attr1" in attributes
        assert "attr2" in attributes
        assert attributes["attr1"]["value"] == "value1"
        assert attributes["attr2"]["value"] == 42

    def test_timer_names(self):
        stats = Stats()
        stats.set_timer("timer1")
        stats.set_timer("timer2")
        assert stats.timer_names() == ["timer1", "timer2"]

    def test_counter_names(self):
        stats = Stats()
        stats.set_counter("counter1")
        stats.set_counter("counter2")
        assert stats.counter_names() == ["counter1", "counter2"]

    def test_ratio_names(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("ratio1", "num", "den")
        stats.set_ratio("ratio2", "num", "den")
        assert stats.ratio_names() == ["ratio1", "ratio2"]

    def test_attribute_names(self):
        stats = Stats()
        stats.set_attribute("attr1", "value")
        stats.set_attribute("attr2", 42)
        assert stats.attribute_names() == ["attr1", "attr2"]

    def test_used_names(self):
        stats = Stats()
        stats.set_timer("timer1")
        stats.set_counter("counter1")
        stats.set_attribute("attr1", "value")
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("ratio1", "num", "den")
        # Should include all names
        used = stats.used_names()
        assert "timer1" in used
        assert "counter1" in used
        assert "attr1" in used
        assert "num" in used
        assert "den" in used
        assert "ratio1" in used
        assert len(used) == 6

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

    def test_set_label(self):
        stats = Stats()
        stats.set_timer("my_timer", "Old Label")
        stats.set_label("my_timer", "New Label")
        assert stats._timers["my_timer"]['label'] == "New Label"

    def test_set_label_counter(self):
        stats = Stats()
        stats.set_counter("my_counter", label="Old Label")
        stats.set_label("my_counter", "New Label")
        assert stats._counters["my_counter"]['label'] == "New Label"

    def test_set_label_ratio(self):
        stats = Stats()
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("my_ratio", "num", "den", "Old Label")
        stats.set_label("my_ratio", "New Label")
        assert stats._ratios["my_ratio"]['label'] == "New Label"

    def test_set_label_attribute(self):
        stats = Stats()
        stats.set_attribute("my_attr", "value", "Old Label")
        stats.set_label("my_attr", "New Label")
        assert stats._attributes["my_attr"]['label'] == "New Label"

    def test_set_label_nonexistent(self):
        stats = Stats()
        with pytest.raises(NameNotExists):
            stats.set_label("nonexistent", "New Label")

    def test_get_labels(self):
        stats = Stats()
        stats.set_timer("timer1", "Timer One")
        stats.set_counter("counter1", label="Counter One")
        stats.set_counter("num")
        stats.set_counter("den")
        stats.set_ratio("ratio1", "num", "den", "Ratio One")
        stats.set_attribute("attr1", "value", "Attribute One")
        
        labels = stats.get_labels()
        expected = {
            "timer1": "Timer One",
            "counter1": "Counter One",
            "num": "num",
            "den": "den",
            "ratio1": "Ratio One",
            "attr1": "Attribute One"
        }
        assert labels == expected

    def test_get_labels_for_timers(self):
        stats = Stats()
        stats.set_timer("timer1", "Timer One")
        stats.set_timer("timer2", "Timer Two")
        stats.set_counter("counter1")  # This shouldn't appear in timer labels
        
        timer_labels = stats.get_labels_for_timers()
        expected = {
            "timer1": "Timer One",
            "timer2": "Timer Two"
        }
        assert timer_labels == expected

    def test_get_labels_for_counters(self):
        stats = Stats()
        stats.set_counter("counter1", label="Counter One")
        stats.set_counter("counter2", label="Counter Two")
        stats.set_timer("timer1")  # This shouldn't appear in counter labels
        
        counter_labels = stats.get_labels_for_counters()
        expected = {
            "counter1": "Counter One",
            "counter2": "Counter Two"
        }
        assert counter_labels == expected

    def test_get_labels_for_ratios(self):
        stats = Stats()
        stats.set_counter("num1")
        stats.set_counter("den1")
        stats.set_counter("num2")
        stats.set_counter("den2")
        stats.set_ratio("ratio1", "num1", "den1", "Ratio One")
        stats.set_ratio("ratio2", "num2", "den2", "Ratio Two")
        stats.set_timer("timer1")  # This shouldn't appear in ratio labels
        
        ratio_labels = stats.get_labels_for_ratios()
        expected = {
            "ratio1": "Ratio One",
            "ratio2": "Ratio Two"
        }
        assert ratio_labels == expected

    def test_get_labels_for_attributes(self):
        stats = Stats()
        stats.set_attribute("attr1", "value1", "Attribute One")
        stats.set_attribute("attr2", "value2", "Attribute Two")
        stats.set_timer("timer1")  # This shouldn't appear in attribute labels
        
        attr_labels = stats.get_labels_for_attributes()
        expected = {
            "attr1": "Attribute One",
            "attr2": "Attribute Two"
        }
        assert attr_labels == expected

    def test_labels_can_be_repeated(self):
        """Test that labels can be repeated across different items"""
        stats = Stats()
        stats.set_timer("timer1", "Same Label")
        stats.set_counter("counter1", label="Same Label")
        stats.set_attribute("attr1", "value", "Same Label")
        
        labels = stats.get_labels()
        assert labels["timer1"] == "Same Label"
        assert labels["counter1"] == "Same Label"
        assert labels["attr1"] == "Same Label"