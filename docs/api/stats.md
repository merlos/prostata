# Stats API Reference

::: prostata.Stats

## Overview

The `Stats` class is the main interface for creating and managing statistics in prostata. It provides methods for creating timers, counters, ratios, and attributes, as well as managing their labels and values.

## Initialization

```python
from prostata import Stats

stats = Stats()
```

## Timer Methods

### set_timer(name, [label])

Create a new timer statistic.

**Parameters:**
- `name` (str): Unique identifier for the timer
- `label` (str, optional): Display label (defaults to name)

**Returns:** None

**Raises:**
- `NameNotAllowed`: If name contains invalid characters
- `NameExists`: If name already exists

**Example:**
```python
stats.set_timer("response_time", "Response Time")
```

### start_timer(name)

Start a timer.

**Parameters:**
- `name` (str): Timer name

**Returns:** None

**Raises:**
- `NameNotExists`: If timer doesn't exist

### stop_timer(name)

Stop a timer and record the duration.

**Parameters:**
- `name` (str): Timer name

**Returns:** float - Duration in seconds

**Raises:**
- `NameNotExists`: If timer doesn't exist

### get_timer(name)

Get the current duration of a timer.

**Parameters:**
- `name` (str): Timer name

**Returns:** float - Duration in seconds

**Raises:**
- `NameNotExists`: If timer doesn't exist

### reset_timer(name)

Reset a timer to zero.

**Parameters:**
- `name` (str): Timer name

**Returns:** None

**Raises:**
- `NameNotExists`: If timer doesn't exist

## Counter Methods

### set_counter(name, initial_value, [label])

Create a new counter statistic.

**Parameters:**
- `name` (str): Unique identifier for the counter
- `initial_value` (int): Starting value
- `label` (str, optional): Display label (defaults to name)

**Returns:** None

**Raises:**
- `NameNotAllowed`: If name contains invalid characters
- `NameExists`: If name already exists

### increment_counter(name, [amount])

Increment a counter.

**Parameters:**
- `name` (str): Counter name
- `amount` (int, optional): Amount to increment (default: 1)

**Returns:** int - New counter value

**Raises:**
- `NameNotExists`: If counter doesn't exist

### decrement_counter(name, [amount])

Decrement a counter.

**Parameters:**
- `name` (str): Counter name
- `amount` (int, optional): Amount to decrement (default: 1)

**Returns:** int - New counter value

**Raises:**
- `NameNotExists`: If counter doesn't exist

### get_counter(name)

Get the current value of a counter.

**Parameters:**
- `name` (str): Counter name

**Returns:** int

**Raises:**
- `NameNotExists`: If counter doesn't exist

### set_counter_value(name, value)

Set a counter to a specific value.

**Parameters:**
- `name` (str): Counter name
- `value` (int): New value

**Returns:** None

**Raises:**
- `NameNotExists`: If counter doesn't exist

### reset_counter(name)

Reset a counter to its initial value.

**Parameters:**
- `name` (str): Counter name

**Returns:** None

**Raises:**
- `NameNotExists`: If counter doesn't exist

## Ratio Methods

### set_ratio(name, initial_value, [label])

Create a new ratio statistic.

**Parameters:**
- `name` (str): Unique identifier for the ratio
- `initial_value` (float): Starting value (typically 0.0 to 1.0)
- `label` (str, optional): Display label (defaults to name)

**Returns:** None

**Raises:**
- `NameNotAllowed`: If name contains invalid characters
- `NameExists`: If name already exists

### get_ratio(name)

Get the current value of a ratio.

**Parameters:**
- `name` (str): Ratio name

**Returns:** float

**Raises:**
- `NameNotExists`: If ratio doesn't exist

### set_ratio_value(name, value)

Set a ratio to a specific value.

**Parameters:**
- `name` (str): Ratio name
- `value` (float): New value

**Returns:** None

**Raises:**
- `NameNotExists`: If ratio doesn't exist

### update_ratio(name, value)

Update a ratio value (same as set_ratio_value).

**Parameters:**
- `name` (str): Ratio name
- `value` (float): New value

**Returns:** None

**Raises:**
- `NameNotExists`: If ratio doesn't exist

### reset_ratio(name)

Reset a ratio to its initial value.

**Parameters:**
- `name` (str): Ratio name

**Returns:** None

**Raises:**
- `NameNotExists`: If ratio doesn't exist

## Attribute Methods

### set_attribute(name, value, [label])

Create a new attribute.

**Parameters:**
- `name` (str): Unique identifier for the attribute
- `value` (Any): Attribute value (any type)
- `label` (str, optional): Display label (defaults to name)

**Returns:** None

**Raises:**
- `NameNotAllowed`: If name contains invalid characters
- `NameExists`: If name already exists

### get_attribute(name)

Get the value of an attribute.

**Parameters:**
- `name` (str): Attribute name

**Returns:** Any - The attribute value

**Raises:**
- `NameNotExists`: If attribute doesn't exist

### set_attribute_value(name, value)

Set an attribute to a new value.

**Parameters:**
- `name` (str): Attribute name
- `value` (Any): New value

**Returns:** None

**Raises:**
- `NameNotExists`: If attribute doesn't exist

### has_attribute(name)

Check if an attribute exists.

**Parameters:**
- `name` (str): Attribute name

**Returns:** bool

## Label Methods

### set_label(name, label)

Set or update the label for any statistic.

**Parameters:**
- `name` (str): Statistic name
- `label` (str): New label

**Returns:** None

**Raises:**
- `NameNotExists`: If statistic doesn't exist

### get_labels()

Get all labels for all statistics.

**Returns:** dict - Mapping of statistic names to labels

### get_labels_for_timers()

Get labels for all timers.

**Returns:** dict - Mapping of timer names to labels

### get_labels_for_counters()

Get labels for all counters.

**Returns:** dict - Mapping of counter names to labels

### get_labels_for_ratios()

Get labels for all ratios.

**Returns:** dict - Mapping of ratio names to labels

### get_labels_for_attributes()

Get labels for all attributes.

**Returns:** dict - Mapping of attribute names to labels

## Utility Methods

### get_all_stats()

Get a summary of all statistics.

**Returns:** dict - Summary with counts by type

### get_timers()

Get all timer names.

**Returns:** list[str]

### get_counters()

Get all counter names.

**Returns:** list[str]

### get_ratios()

Get all ratio names.

**Returns:** list[str]

### get_attributes()

Get all attribute names and values.

**Returns:** dict - Mapping of attribute names to values

### has_timer(name)

Check if a timer exists.

**Parameters:**
- `name` (str): Timer name

**Returns:** bool

### has_counter(name)

Check if a counter exists.

**Parameters:**
- `name` (str): Counter name

**Returns:** bool

### has_ratio(name)

Check if a ratio exists.

**Parameters:**
- `name` (str): Ratio name

**Returns:** bool

## Exceptions

### NameNotAllowed

Raised when a statistic name contains invalid characters.

**Valid characters:** Letters, numbers, and underscores. Must start with a letter or underscore.

### NameExists

Raised when trying to create a statistic with a name that already exists.

### NameNotExists

Raised when trying to access a statistic that doesn't exist.