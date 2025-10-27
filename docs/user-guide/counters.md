# Counters

Counters track quantities or event counts with increment and decrement operations.

## Creating Counters

```python
from prostata import Stats

stats = Stats()

# Create a counter with default values
stats.set_counter("requests")

# Create a counter with initial value and unit
stats.set_counter("bytes_processed", 0, "bytes", "Bytes Processed")

# Create a counter with custom label
stats.set_counter("errors", 0, "count", "Error Count")
```

## Using Counters

```python
# Increment by 1
stats.incr("requests")
# or using dynamic method:
stats.incr_requests()

# Increment by specific amount
stats.incr("bytes_processed", 1024)
# or using dynamic method:
stats.incr_bytes_processed(1024)

# Decrement by 1
stats.decr("requests")
# or using dynamic method:
stats.decr_requests()

# Decrement by specific amount
stats.decr("bytes_processed", 100)

# Get current value
count = stats.get_counter("requests")
# or using dynamic method:
count = stats.get_requests()

# Reset to specific value
stats.reset_counter("requests", 0)
# or using dynamic method:
stats.reset_requests(0)

# Change unit
stats.set_counter_unit("bytes_processed", "MB")
```

## Counter Features

### Units
Counters can have units for better context:

```python
stats.set_counter("memory_usage", 0, "MB", "Memory Usage (MB)")
stats.set_counter("api_calls", 0, "requests", "API Call Count")
stats.set_counter("files_processed", 0, "files", "Files Processed")
```

### Thread Safety
!!! warning "Thread Safety"
    Counters are not thread-safe by default. If you need to use counters across multiple threads, implement your own locking mechanism.

### Negative Values
Counters can go negative:

```python
stats.set_counter("balance", 100)
stats.decr_balance(150)  # balance = -50
```

## Counter Labels

```python
# Get all counter labels
counter_labels = stats.get_labels_for_counters()

# Update a counter label
stats.set_label("requests", "HTTP Requests")
```