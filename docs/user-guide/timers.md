# Timers

Timers allow you to track elapsed time between start and stop events.

## Creating Timers

```python
from prostata import Stats

stats = Stats()

# Create a timer with default label
stats.set_timer("response_time")

# Create a timer with custom label
stats.set_timer("db_query", "Database Query Time")
```

## Using Timers

```python
# Start timing
stats.start_timer("response_time")
# or using dynamic method:
stats.start_response_time()

# Do some work
import time
time.sleep(0.1)

# Stop timing
stats.stop_timer("response_time")
# or using dynamic method:
stats.stop_response_time()

# Get elapsed time in seconds
elapsed = stats.get_timer("response_time")
# or using dynamic method:
elapsed = stats.get_response_time()

print(f"Elapsed time: {elapsed:.2f} seconds")
```

## Timer Features

### Multiple Segments
Timers can be started and stopped multiple times, accumulating total time:

```python
stats.set_timer("work_time")

stats.start_work_time()
time.sleep(0.1)
stats.stop_work_time()

stats.start_work_time()
time.sleep(0.2)
stats.stop_work_time()

total_time = stats.get_work_time()  # 0.3 seconds
```

### Running Timers
You can check elapsed time while a timer is still running:

```python
stats.set_timer("operation")
stats.start_operation()

time.sleep(0.5)
current_elapsed = stats.get_operation()  # ~0.5 seconds

time.sleep(0.5)
stats.stop_operation()
final_elapsed = stats.get_operation()  # ~1.0 seconds
```

### Never Started Timers
Timers that haven't been started return 0:

```python
stats.set_timer("unused")
elapsed = stats.get_unused()  # 0.0
```

## Timer Labels

```python
# Get all timer labels
timer_labels = stats.get_labels_for_timers()
print(timer_labels)  # {'response_time': 'response_time', 'db_query': 'Database Query Time'}

# Update a timer label
stats.set_label("response_time", "HTTP Response Time")
```