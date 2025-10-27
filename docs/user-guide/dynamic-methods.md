# Dynamic Methods

Prostata automatically generates dynamic methods for all your statistics, providing convenient shortcuts for common operations.

## Generated Methods

For each statistic you create, prostata generates several methods automatically:

### Timer Methods

```python
stats.set_timer("response_time")

# Generated methods:
stats.start_response_time()     # Start the timer
stats.stop_response_time()      # Stop the timer and record duration
stats.get_response_time()       # Get the current duration
stats.reset_response_time()     # Reset the timer
```

### Counter Methods

```python
stats.set_counter("requests", 0)

# Generated methods:
stats.inc_requests()            # Increment by 1
stats.inc_requests(5)           # Increment by 5
stats.dec_requests()            # Decrement by 1
stats.dec_requests(3)           # Decrement by 3
stats.get_requests()            # Get current value
stats.set_requests(100)         # Set to specific value
stats.reset_requests()          # Reset to initial value
```

### Ratio Methods

```python
stats.set_ratio("hit_rate", 0.0)

# Generated methods:
stats.get_hit_rate()            # Get current ratio
stats.set_hit_rate(0.95)        # Set ratio value
stats.update_hit_rate(0.92)     # Update ratio (same as set)
stats.reset_hit_rate()          # Reset to initial value
```

### Attribute Methods

```python
stats.set_attribute("version", "1.0.0")

# Generated methods:
stats.get_version()             # Get attribute value
stats.set_version("1.1.0")      # Set attribute value
```

## Method Naming Convention

Dynamic methods follow this pattern:

- `start_<name>()` - Start a timer
- `stop_<name>()` - Stop a timer
- `get_<name>()` - Get the current value
- `set_<name>(value)` - Set a new value
- `reset_<name>()` - Reset to initial value
- `inc_<name>([amount])` - Increment a counter (default amount=1)
- `dec_<name>([amount])` - Decrement a counter (default amount=1)
- `update_<name>(value)` - Update a ratio (same as set)

## Examples

### Web Server Monitoring

```python
from prostata import Stats

stats = Stats()

# Set up statistics
stats.set_counter("requests_total", 0, "Total Requests")
stats.set_counter("errors_total", 0, "Total Errors")
stats.set_timer("request_duration", "Request Duration")
stats.set_ratio("error_rate", 0.0, "Error Rate")
stats.set_attribute("server_status", "running", "Server Status")

# Handle a request
stats.inc_requests_total()           # requests_total += 1
stats.start_request_duration()       # Start timing

# ... process request ...

if error_occurred:
    stats.inc_errors_total()         # errors_total += 1

stats.stop_request_duration()        # Stop timing

# Update error rate
total_requests = stats.get_requests_total()
total_errors = stats.get_errors_total()
stats.set_error_rate(total_errors / total_requests if total_requests > 0 else 0)

# Check server status
status = stats.get_server_status()  # "running"
```

### Database Connection Pool

```python
# Set up pool statistics
stats.set_counter("connections_active", 0, "Active Connections")
stats.set_counter("connections_created", 0, "Connections Created")
stats.set_attribute("pool_size", 10, "Pool Size")

def get_connection():
    stats.inc_connections_active()
    stats.inc_connections_created()
    # ... get connection logic ...
    return connection

def release_connection(conn):
    stats.dec_connections_active()
    # ... release logic ...

# Usage
conn1 = get_connection()  # active: 1, created: 1
conn2 = get_connection()  # active: 2, created: 2
release_connection(conn1) # active: 1
```

## Benefits

### Convenience
Dynamic methods provide shortcuts without remembering method names:

```python
# Instead of:
stats.increment_counter("requests", 1)
stats.set_attribute_value("status", "busy")

# You can use:
stats.inc_requests()
stats.set_status("busy")
```

### Type Safety
Methods are generated based on the statistic type, providing appropriate operations:

```python
# Timers get start/stop methods
stats.start_response_time()
stats.stop_response_time()

# Counters get inc/dec methods
stats.inc_requests()
stats.dec_requests()

# Ratios get update methods
stats.update_hit_rate(0.95)
```

### IDE Support
Dynamic methods enable better IDE autocompletion and type checking.

## Method Availability

Dynamic methods are available immediately after creating a statistic:

```python
stats = Stats()

# Method doesn't exist yet
# stats.get_my_counter()  # AttributeError

stats.set_counter("my_counter", 0)

# Now the method exists
stats.get_my_counter()  # 0
stats.inc_my_counter()  # 1
```

## Error Handling

If you try to use a dynamic method for a non-existent statistic, you'll get an `AttributeError`:

```python
stats = Stats()
stats.get_unknown_stat()  # AttributeError: 'Stats' object has no attribute 'get_unknown_stat'
```

Use the main API methods if you need to handle missing statistics gracefully:

```python
# Safe access
try:
    value = stats.get_my_stat()
except AttributeError:
    value = None

# Or use the main API
if stats.has_counter("my_stat"):
    value = stats.get_counter("my_stat")
```