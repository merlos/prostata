# Getting Started

Welcome to prostata! This guide will help you get started with tracking statistics in your Python applications.

## Installation

Install prostata using pip:

```bash
pip install prostata
```

## Basic Usage

```python
from prostata import Stats

# Create a stats instance
stats = Stats()

# Create different types of statistics
stats.set_timer("operation_time", "Operation Duration")
stats.set_counter("items_processed", 0, "count", "Items Processed")
stats.set_attribute("version", "1.0.0", "Application Version")

# Use the statistics
stats.start_operation_time()
# ... do some work ...
stats.incr_items_processed(5)
stats.stop_operation_time()

# Get results
duration = stats.get_operation_time()
count = stats.get_items_processed()
version = stats.get_version()
```

## Types of Statistics

### Timers
Track elapsed time between start and stop events.

### Counters
Count occurrences or quantities with increment/decrement operations.

### Ratios
Calculate ratios between two counters automatically.

### Attributes
Store arbitrary values and metadata.

## Labels

All statistics can have descriptive labels that default to their names:

```python
# Custom label
stats.set_timer("db_query", "Database Query Time")

# Default label (same as name)
stats.set_counter("requests")  # label = "requests"
```

## Dynamic Methods

prostata automatically creates convenient methods for each statistic:

```python
stats.set_timer("load_time")
stats.set_counter("items")

# These methods are created automatically:
stats.start_load_time()    # instead of stats.start_timer("load_time")
stats.incr_items()         # instead of stats.incr("items")
```

## Next Steps

- Learn about [Timers](timers.md)
- Learn about [Counters](counters.md)
- Learn about [Ratios](ratios.md)
- Learn about [Attributes](attributes.md)
- Learn about [Labels](labels.md)
- Check the [API Reference](../api/stats.md)