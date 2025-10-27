# Ratios

Ratios calculate the relationship between two counters automatically.

## Creating Ratios

```python
from prostata import Stats

stats = Stats()

# Create the counters first
stats.set_counter("success", 95, "count", "Successful Operations")
stats.set_counter("total", 100, "count", "Total Operations")

# Create a ratio
stats.set_ratio("success_rate", "success", "total", "Success Rate")
```

## Using Ratios

```python
# Update counter values
stats.incr_success(5)  # success = 100
stats.incr_total(10)   # total = 110

# Get the ratio (calculated automatically)
rate = stats.get_ratio("success_rate")
# or using dynamic method:
rate = stats.get_success_rate()

print(f"Success rate: {rate:.1%}")  # Success rate: 90.9%
```

## Ratio Features

### Automatic Calculation
Ratios are calculated on-demand using the current counter values:

```python
# Ratio = numerator / denominator
# If denominator = 0, ratio = 0.0

stats.set_counter("errors", 3)
stats.set_counter("requests", 100)
stats.set_ratio("error_rate", "errors", "requests")

print(stats.get_error_rate())  # 0.03
```

### Dynamic Updates
Ratios reflect current counter values:

```python
stats.set_counter("passed", 8)
stats.set_counter("total", 10)
stats.set_ratio("pass_rate", "passed", "total")

print(stats.get_pass_rate())  # 0.8

stats.incr_passed(1)
stats.incr_total(1)
print(stats.get_pass_rate())  # 0.818...
```

### Use Cases

Common ratio patterns:

```python
# Error rates
stats.set_ratio("error_rate", "errors", "requests")

# Success rates
stats.set_ratio("success_rate", "success", "attempts")

# Cache hit rates
stats.set_ratio("cache_hit_rate", "cache_hits", "cache_requests")

# Conversion rates
stats.set_ratio("conversion_rate", "conversions", "visitors")
```

## Ratio Labels

```python
# Get all ratio labels
ratio_labels = stats.get_labels_for_ratios()

# Update a ratio label
stats.set_label("success_rate", "Operation Success Rate")
```