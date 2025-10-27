# prostata

[![PyPI version](https://badge.fury.io/py/prostata.svg)](https://pypi.org/project/prostata/)
[![Python versions](https://img.shields.io/pypi/pyversions/prostata.svg)](https://pypi.org/project/prostata/)

A Python library for **PRO**cessing **STAT**istics with timers, counters, ratios, and attributes.

## Features

- **Timers**: Track elapsed time with start/stop functionality
- **Counters**: Count events with increment/decrement operations
- **Ratios**: Calculate ratios between counters automatically
- **Attributes**: Store arbitrary values and metadata
- **Labels**: Add descriptive labels to all statistics
- **Dynamic Methods**: Auto-generated methods for easy access
- **Type Safety**: Full type hints and validation

## Quick Start

```python
from prostata import Stats

# Create a stats instance
stats = Stats()

# Create a timer
stats.set_timer("response_time", "Response Time")

# Create counters
stats.set_counter("requests", 0, "count", "Total Requests")
stats.set_counter("errors", 0, "count", "Error Count")

# Start timing
stats.start_response_time()

# Simulate work
import time
time.sleep(0.1)

# Increment counters
stats.incr_requests()
stats.incr_errors(2)

# Stop timing
stats.stop_response_time()

# Get results
print(f"Response time: {stats.get_response_time():.2f} seconds")
print(f"Requests: {stats.get_requests()}")
print(f"Errors: {stats.get_errors()}")

# Create a ratio
stats.set_ratio("error_rate", "errors", "requests", "Error Rate")
print(f"Error rate: {stats.get_error_rate():.2%}")
```

## Installation

```bash
pip install prostata
```

## Documentation

- [Getting Started](user-guide/getting-started.md)
- [API Reference](api/stats.md)
- [Contributing](development/contributing.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/merlos/prostata/blob/main/LICENSE) file for details.