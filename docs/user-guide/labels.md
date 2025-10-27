# Labels

Labels provide descriptive names for your statistics, making them more readable and self-documenting.

## Creating Labels

Labels are set when creating statistics and default to the statistic name:

```python
from prostata import Stats

stats = Stats()

# Default labels (same as name)
stats.set_timer("response_time")        # label = "response_time"
stats.set_counter("requests")           # label = "requests"

# Custom labels
stats.set_timer("db_query", "Database Query Time")
stats.set_counter("errors", 0, "count", "Error Count")
stats.set_attribute("version", "1.0.0", "Application Version")
```

## Managing Labels

```python
# Update existing labels
stats.set_label("response_time", "HTTP Response Time")
stats.set_label("requests", "Total HTTP Requests")

# Get labels for specific types
timer_labels = stats.get_labels_for_timers()
counter_labels = stats.get_labels_for_counters()
ratio_labels = stats.get_labels_for_ratios()
attr_labels = stats.get_labels_for_attributes()

# Get all labels
all_labels = stats.get_labels()
```

## Label Features

### Uniqueness
Names must be unique across all statistic types, but labels can be repeated:

```python
# This works - same label, different names/types
stats.set_timer("query_time", "Database Operation")
stats.set_counter("query_count", "Database Operation")
stats.set_attribute("query_status", "idle", "Database Operation")
```

### Display Names
Labels are useful for display purposes:

```python
# Instead of showing technical names:
print("Statistics:")
for name, label in stats.get_labels().items():
    value = getattr(stats, f'get_{name}')()
    print(f"  {label}: {value}")
```

Output:
```
Statistics:
  HTTP Response Time: 0.123
  Total HTTP Requests: 42
  Error Count: 2
  Application Version: 1.0.0
```

### Internationalization
Labels can be used for i18n:

```python
# English
stats.set_timer("response_time", "Response Time")

# Spanish
stats.set_timer("response_time", "Tiempo de Respuesta")

# French
stats.set_timer("response_time", "Temps de Réponse")
```

## Best Practices

### Descriptive Labels
Use clear, descriptive labels:

```python
# Good
stats.set_counter("http_requests", "HTTP Requests")
stats.set_timer("db_query_time", "Database Query Duration")

# Less clear
stats.set_counter("req", "req")
stats.set_timer("time", "time")
```

### Consistent Naming
Establish naming conventions for your project:

```python
# Consistent patterns
stats.set_counter("cache_hits", "Cache Hits")
stats.set_counter("cache_misses", "Cache Misses")
stats.set_counter("cache_hit_rate", "Cache Hit Rate")  # ratio

# Or with prefixes
stats.set_counter("http_requests_total", "Total HTTP Requests")
stats.set_counter("http_requests_errors", "HTTP Error Requests")
```

### Label Updates
Labels can be updated at runtime:

```python
stats.set_attribute("status", "initializing", "System Status")

# Later...
stats.set_label("status", "System Health Status")
stats.set_attribute_value("status", "healthy")
```