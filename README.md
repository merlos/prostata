# prostata

A Python library for PROcessing STATistics with timers, counters, ratios, and attributes.

## Installation

```bash
pip install .
```

## Usage

```python
from prostata import Stats

# Create a stats instance
stats = Stats()

# Create a timer
stats.set_timer("response_time")

# Create counters
stats.set_counter("requests", 0, "count")
stats.set_counter("errors", 0, "count")

# Create an attribute
stats.set_attribute("version", "1.0.0")

# Start timing
stats.start_timer("response_time")

# Simulate some work
import time
time.sleep(0.1)

# Increment counters
stats.incr("requests")
stats.incr("errors")

# Stop timing
stats.stop_timer("response_time")

# Get values
print(f"Response time: {stats.get_timer('response_time'):.2f} seconds")
print(f"Requests: {stats.get_counter('requests')}")
print(f"Errors: {stats.get_counter('errors')}")
print(f"Version: {stats.get_attribute('version')}")

# Create a ratio
stats.set_ratio("error_rate", "errors", "requests")
print(f"Error rate: {stats.get_ratio('error_rate'):.2%}")

# Use dynamic methods
stats.start_response_time()  # equivalent to start_timer("response_time")
stats.incr_requests()        # equivalent to incr("requests")
print(f"Response time via dynamic method: {stats.get_response_time():.2f} seconds")
```

## Features

### Timers
Track elapsed time with start/stop functionality:

```python
stats.set_timer("operation_time")
stats.start_timer("operation_time")
# ... do work ...
stats.stop_timer("operation_time")
elapsed = stats.get_timer("operation_time")
```

### Counters
Count events with units:

```python
stats.set_counter("bytes_processed", 0, "bytes")
stats.incr("bytes_processed", 1024)
stats.decr("bytes_processed", 100)
current = stats.get_counter("bytes_processed")
```

### Ratios
Calculate ratios between counters:

```python
stats.set_counter("success", 95)
stats.set_counter("total", 100)
stats.set_ratio("success_rate", "success", "total")
rate = stats.get_ratio("success_rate")  # 0.95
```

### Attributes
Store arbitrary values:

```python
stats.set_attribute("config", {"debug": True})
stats.set_attribute("timeout", 30)
value = stats.get_attribute("config")
```

### Dynamic Methods
Each stat creates dynamic methods for easy access:

```python
stats.set_timer("load_time")
stats.set_counter("items")
stats.set_attribute("status")

# Dynamic methods are automatically created
stats.start_load_time()
stats.incr_items()
stats.set_status("running")
```

### Name Validation
- Names must be unique across all stat types
- Reserved words: "timer", "counter", "ratio", "attribute"
- Raises `NameExists` if name is already used
- Raises `NameNotAllowed` for reserved words

## Exceptions

- `NameNotAllowed`: When using reserved names
- `NameExists`: When name is already in use
- `NameNotExists`: When accessing non-existent stats

## Development

To install in development mode:

```bash
pip install -e .[dev]
```

To run tests:

```bash
python -m pytest
```

To run tests with coverage:

```bash
python -m pytest --cov=prostata --cov-report term-missing
```