from datetime import datetime
from typing import Union
import re


class NameNotAllowed(Exception):
    pass


class NameExists(Exception):
    pass


class NameNotExists(Exception):
    pass


class Stats:

    def __init__(self):
        self._timers = {}  # {name: {'start': datetime, 'stop': datetime, segments: int ,'elapsed': duration, 'label': str}}
        self._counters = {}  # {name: {'value': amount, 'unit': unit, 'label': str}}
        self._ratios = {}  # {name: {'numerator': name, 'denominator': name, 'value': ratio, 'label': str}}
        self._attributes = {}  # {name: {'value': value, 'label': str}}
        self._names_used = set()  # Track all names to ensure uniqueness

    def is_used(self, name: str) -> bool:
        """
        Check if a name is being used across timers, counters, ratios, and attributes.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is used, False otherwise.
        """
        return name in self._names_used

    def _check_name_allowed(self, name: str):
        """
        Check if the name is allowed (not a reserved word and valid format).
        Args:
            name (str): The name to check.
        Returns:
            None
        Raises:
            NameNotAllowed: If the name is a reserved word or has invalid format.
        """
        forbidden = ["timer", "counter", "ratio", "attribute", "timers", "counters", "ratios", "attributes"]
        if name in forbidden:
            raise NameNotAllowed(f"Name '{name}' is not allowed as it is a reserved word (timer, counter, ratio, attribute are reserved).")
        if not re.match(r'^[a-z0-9_]+$', name):
            raise NameNotAllowed(f"Name '{name}' contains invalid characters. Only lowercase letters, digits, and underscores are allowed.")

    def _check_name_unique(self, name: str):
        """ 
        Check if the name is unique across timers, counters, ratios, and attributes.
        Args:
            name (str): The name to check.
        Returns:
            None
        Raises:
            NameExists: If the name is already used.
        """
        if self.is_used(name):
            raise NameExists(f"Name '{name}' already exists. Names cannot be repeated across timers, counters, ratios, and attributes.")

    def set_timer(self, name: str, label: str = None):
        """
        Create a new timer with the given name.

        Args:
            name (str): The name of the timer.
            label (str, optional): The label for the timer. Defaults to the name if not provided.

        Raises:
            NameNotAllowed: If the name is a reserved word or has invalid format.
            NameExists: If the name is already used.
        """
        self._check_name_allowed(name)
        self._check_name_unique(name)
        if label is None:
            label = name
        self._timers[name] = {'start': None, 'stop': None, 'segments': 0, 'elapsed': 0.0, 'label': label}
        self._names_used.add(name)
        # Add dynamic methods
        setattr(self, f'get_{name}', lambda: self.get_timer(name))
        setattr(self, f'start_{name}', lambda: self.start_timer(name))
        setattr(self, f'stop_{name}', lambda: self.stop_timer(name))

    def set_counter(self, name: str, value: int = 0, unit: str = "item", label: str = None):
        """
        Create a new counter with the given name, initial value, and unit.

        Args:
            name (str): The name of the counter.
            value (int): The initial value. Defaults to 0.
            unit (str): The unit of the counter. Defaults to "item".
            label (str, optional): The label for the counter. Defaults to the name if not provided.

        Raises:
            NameNotAllowed: If the name is a reserved word or has invalid format.
            NameExists: If the name is already used.
        """
        self._check_name_allowed(name)
        self._check_name_unique(name)
        if label is None:
            label = name
        self._counters[name] = {'value': value, 'unit': unit, 'label': label}
        self._names_used.add(name)
        # Add dynamic methods
        setattr(self, f'get_{name}', lambda: self.get_counter(name))
        setattr(self, f'incr_{name}', lambda amount=1: self.incr(name, amount))
        setattr(self, f'decr_{name}', lambda amount=1: self.decr(name, amount))
        setattr(self, f'reset_{name}', lambda value=0: self.reset_counter(name, value))

    def set_ratio(self, name: str, numerator: str, denominator: str, label: str = None):
        """
        Create a new ratio with the given name, numerator, and denominator.

        Args:
            name (str): The name of the ratio.
            numerator (str): The name of the numerator counter.
            denominator (str): The name of the denominator counter.
            label (str, optional): The label for the ratio. Defaults to the name if not provided.

        Raises:
            NameNotAllowed: If the name is a reserved word or has invalid format.
            NameExists: If the name is already used.
            NameNotExists: If numerator or denominator do not exist.
        """
        self._check_name_allowed(name)
        self._check_name_unique(name)
        if not self.is_used(numerator):
            raise NameNotExists(f"Numerator '{numerator}' does not exist.")
        if not self.is_used(denominator):
            raise NameNotExists(f"Denominator '{denominator}' does not exist.")
        if label is None:
            label = name
        self._ratios[name] = {'numerator': numerator, 'denominator': denominator, 'value': 0.0, 'label': label}
        self._names_used.add(name)
        # Add dynamic method
        setattr(self, f'get_{name}', lambda: self.get_ratio(name))

    def set_attribute(self, name: str, value: Union[str, int, float] = "", label: str = None):
        """
        Create a new attribute with the given name and value.

        Args:
            name (str): The name of the attribute.
            value (Union[str, int, float]): The value of the attribute. Defaults to "".
            label (str, optional): The label for the attribute. Defaults to the name if not provided.

        Raises:
            NameNotAllowed: If the name is a reserved word or has invalid format.
            NameExists: If the name is already used.
        """
        self._check_name_allowed(name)
        self._check_name_unique(name)
        if label is None:
            label = name
        self._attributes[name] = {'value': value, 'label': label}
        self._names_used.add(name)
        # Add dynamic method
        setattr(self, f'get_{name}', lambda: self.get_attribute(name))
        setattr(self, f'set_{name}', lambda value: self.set_attribute_value(name, value))

    def get_timer(self, name: str) -> float:
        """
        Get the elapsed time in seconds for the timer.

        Args:
            name (str): The name of the timer.

        Returns:
            float: The elapsed time in seconds. Returns 0 if never started.

        Raises:
            NameNotExists: If the timer does not exist.
        """
        if name not in self._timers:
            raise NameNotExists(f"Timer '{name}' does not exist.")
        timer = self._timers[name]
        elapsed = timer['elapsed']
        if timer['start'] is not None:
            elapsed += (datetime.now() - timer['start']).total_seconds()
        return elapsed

    def start_timer(self, name: str):
        """
        Start the timer.

        Args:
            name (str): The name of the timer.

        Raises:
            NameNotExists: If the timer does not exist.
        """
        if name not in self._timers:
            raise NameNotExists(f"Timer '{name}' does not exist.")
        timer = self._timers[name]
        if timer['start'] is None:
            timer['start'] = datetime.now()
            timer['segments'] += 1

    def stop_timer(self, name: str):
        """
        Stop the timer and accumulate elapsed time.

        Args:
            name (str): The name of the timer.

        Raises:
            NameNotExists: If the timer does not exist.
        """
        if name not in self._timers:
            raise NameNotExists(f"Timer '{name}' does not exist.")
        timer = self._timers[name]
        if timer['start'] is not None:
            now = datetime.now()
            timer['elapsed'] += (now - timer['start']).total_seconds()
            timer['stop'] = now
            timer['start'] = None

    def get_counter(self, name: str) -> int:
        """
        Get the value of the counter.

        Args:
            name (str): The name of the counter.

        Returns:
            int: The value of the counter.

        Raises:
            NameNotExists: If the counter does not exist.
        """
        if name not in self._counters:
            raise NameNotExists(f"Counter '{name}' does not exist.")
        return self._counters[name]['value']

    def incr(self, name: str, amount: int = 1):
        """
        Increment the counter by the given amount.

        Args:
            name (str): The name of the counter.
            amount (int): The amount to increment. Defaults to 1.

        Raises:
            NameNotExists: If the counter does not exist.
        """
        if name not in self._counters:
            raise NameNotExists(f"Counter '{name}' does not exist.")
        self._counters[name]['value'] += amount

    def decr(self, name: str, amount: int = 1):
        """
        Decrement the counter by the given amount.

        Args:
            name (str): The name of the counter.
            amount (int): The amount to decrement. Defaults to 1.

        Raises:
            NameNotExists: If the counter does not exist.
        """
        if name not in self._counters:
            raise NameNotExists(f"Counter '{name}' does not exist.")
        self._counters[name]['value'] -= amount

    def reset_counter(self, name: str, value: int = 0):
        """
        Reset the counter to the given value.

        Args:
            name (str): The name of the counter.
            value (int): The value to reset to. Defaults to 0.

        Raises:
            NameNotExists: If the counter does not exist.
        """
        if name not in self._counters:
            raise NameNotExists(f"Counter '{name}' does not exist.")
        self._counters[name]['value'] = value

    def set_counter_unit(self, name: str, unit: str):
        """
        Set the unit of the counter.

        Args:
            name (str): The name of the counter.
            unit (str): The new unit.

        Raises:
            NameNotExists: If the counter does not exist.
        """
        if name not in self._counters:
            raise NameNotExists(f"Counter '{name}' does not exist.")
        self._counters[name]['unit'] = unit

    def get_ratio(self, name: str) -> float:
        """
        Get the value of the ratio.

        Args:
            name (str): The name of the ratio.

        Returns:
            float: The ratio value. Returns 0 if denominator is 0.

        Raises:
            NameNotExists: If the ratio does not exist.
        """
        if name not in self._ratios:
            raise NameNotExists(f"Ratio '{name}' does not exist.")
        ratio = self._ratios[name]
        num_value = self.get_counter(ratio['numerator'])
        den_value = self.get_counter(ratio['denominator'])
        if den_value == 0:
            return 0.0
        return num_value / den_value

    def get_attribute(self, name: str) -> Union[str, int, float]:
        """
        Get the value of the attribute.

        Args:
            name (str): The name of the attribute.

        Returns:
            Union[str, int, float]: The value of the attribute.

        Raises:
            NameNotExists: If the attribute does not exist.
        """
        if name not in self._attributes:
            raise NameNotExists(f"Attribute '{name}' does not exist.")
        return self._attributes[name]['value']

    def set_attribute_value(self, name: str, value: Union[str, int, float]):
        """
        Set the value of the attribute.

        Args:
            name (str): The name of the attribute.
            value (Union[str, int, float]): The new value.

        Raises:
            NameNotExists: If the attribute does not exist.
        """
        if name not in self._attributes:
            raise NameNotExists(f"Attribute '{name}' does not exist.")
        self._attributes[name]['value'] = value

    def get_timers(self) -> dict:
        """
        Get all timers.

        Returns:
            dict: A copy of the timers dictionary.
        """
        return self._timers.copy()

    def get_counters(self) -> dict:
        """
        Get all counters.

        Returns:
            dict: A copy of the counters dictionary.
        """
        return self._counters.copy()

    def get_ratios(self) -> dict:
        """
        Get all ratios.

        Returns:
            dict: A copy of the ratios dictionary.
        """
        return self._ratios.copy()

    def get_attributes(self) -> dict:
        """
        Get all attributes.

        Returns:
            dict: A copy of the attributes dictionary.
        """
        return self._attributes.copy()

    def timer_names(self) -> list:
        """
        Get the list of timer names.

        Returns:
            list: A list of timer names.
        """
        return list(self._timers.keys())

    def counter_names(self) -> list:
        """
        Get the list of counter names.

        Returns:
            list: A list of counter names.
        """
        return list(self._counters.keys())

    def ratio_names(self) -> list:
        """
        Get the list of ratio names.

        Returns:
            list: A list of ratio names.
        """
        return list(self._ratios.keys())

    def attribute_names(self) -> list:
        """
        Get the list of attribute names.

        Returns:
            list: A list of attribute names.
        """
        return list(self._attributes.keys())

    def used_names(self) -> list:
        """
        Get the list of all used names.

        Returns:
            list: A list of all used names across timers, counters, ratios, and attributes.
        """
        return list(self._names_used)

    def set_label(self, name: str, new_label: str):
        """
        Set a new label for an existing timer, counter, ratio, or attribute.

        Args:
            name (str): The name of the item to update.
            new_label (str): The new label to set.

        Raises:
            NameNotExists: If the name does not exist.
        """
        if not self.is_used(name):
            raise NameNotExists(f"Name '{name}' does not exist.")
        
        if name in self._timers:
            self._timers[name]['label'] = new_label
        elif name in self._counters:
            self._counters[name]['label'] = new_label
        elif name in self._ratios:
            self._ratios[name]['label'] = new_label
        elif name in self._attributes:
            self._attributes[name]['label'] = new_label

    def get_labels(self) -> dict:
        """
        Get all name/label pairs for all items.

        Returns:
            dict: A dictionary mapping names to their labels.
        """
        labels = {}
        for name, timer in self._timers.items():
            labels[name] = timer['label']
        for name, counter in self._counters.items():
            labels[name] = counter['label']
        for name, ratio in self._ratios.items():
            labels[name] = ratio['label']
        for name, attr in self._attributes.items():
            labels[name] = attr['label']
        return labels

    def get_labels_for_timers(self) -> dict:
        """
        Get all name/label pairs for timers.

        Returns:
            dict: A dictionary mapping timer names to their labels.
        """
        return {name: timer['label'] for name, timer in self._timers.items()}

    def get_labels_for_counters(self) -> dict:
        """
        Get all name/label pairs for counters.

        Returns:
            dict: A dictionary mapping counter names to their labels.
        """
        return {name: counter['label'] for name, counter in self._counters.items()}

    def get_labels_for_ratios(self) -> dict:
        """
        Get all name/label pairs for ratios.

        Returns:
            dict: A dictionary mapping ratio names to their labels.
        """
        return {name: ratio['label'] for name, ratio in self._ratios.items()}

    def get_labels_for_attributes(self) -> dict:
        """
        Get all name/label pairs for attributes.

        Returns:
            dict: A dictionary mapping attribute names to their labels.
        """
        return {name: attr['label'] for name, attr in self._attributes.items()}
