# Attributes

Attributes store arbitrary values and metadata.

## Creating Attributes

```python
from prostata import Stats

stats = Stats()

# Create attributes with different value types
stats.set_attribute("version", "1.2.3", "Application Version")
stats.set_attribute("debug_mode", True, "Debug Mode Enabled")
stats.set_attribute("timeout", 30, "Request Timeout (seconds)")
stats.set_attribute("config", {"host": "localhost", "port": 8080}, "Server Configuration")
```

## Using Attributes

```python
# Get attribute values
version = stats.get_attribute("version")
debug = stats.get_attribute("debug_mode")
timeout = stats.get_attribute("timeout")
config = stats.get_attribute("config")

# Update attribute values
stats.set_attribute_value("version", "1.2.4")
# or using dynamic method:
stats.set_version("1.2.4")
```

## Attribute Features

### Type Flexibility
Attributes can store any Python value:

```python
# Simple types
stats.set_attribute("count", 42)
stats.set_attribute("rate", 0.95)
stats.set_attribute("name", "my_app")

# Complex types
stats.set_attribute("settings", {
    "debug": True,
    "log_level": "INFO",
    "features": ["auth", "cache", "metrics"]
})

stats.set_attribute("callback", lambda x: x * 2)
```

### Dynamic Setters
Like other statistics, attributes get dynamic setter methods:

```python
stats.set_attribute("status", "initializing")

# These methods are created automatically:
stats.set_status("running")    # instead of stats.set_attribute_value("status", "running")
```

### Use Cases

Attributes are useful for:

- Configuration values
- Metadata about your application
- Status information
- Computed values that don't fit counters/ratios
- Complex data structures

```python
# Application metadata
stats.set_attribute("app_name", "MyApp")
stats.set_attribute("start_time", datetime.now())
stats.set_attribute("environment", "production")

# Runtime configuration
stats.set_attribute("max_connections", 100)
stats.set_attribute("cache_enabled", True)

# Status information
stats.set_attribute("health_status", "healthy")
stats.set_attribute("last_error", None)
```

## Attribute Labels

```python
# Get all attribute labels
attr_labels = stats.get_labels_for_attributes()

# Update an attribute label
stats.set_label("version", "Application Version Number")
```