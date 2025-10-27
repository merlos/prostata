# Testing

Prostata uses comprehensive testing to ensure reliability and maintain code quality.

## Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── __init__.py
└── test_prostata.py
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_prostata.py

# Run specific test class
pytest tests/test_prostata.py::TestStats

# Run specific test method
pytest tests/test_prostata.py::TestStats::test_set_timer
```

### Coverage Reporting

```bash
# Generate coverage report
pytest --cov=prostata

# Generate HTML coverage report
pytest --cov=prostata --cov-report=html

# View HTML report (opens in browser)
open htmlcov/index.html
```

### Test Configuration

Tests use `pytest` with the following configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
]
```

## Test Categories

### Unit Tests

Unit tests cover individual components and methods:

- **Timer Tests**: Test timer creation, starting, stopping, and duration calculation
- **Counter Tests**: Test counter creation, incrementing, decrementing, and value setting
- **Ratio Tests**: Test ratio creation, value setting, and updating
- **Attribute Tests**: Test attribute creation, value getting/setting, and type handling
- **Label Tests**: Test label setting, updating, and retrieval for all statistic types
- **Dynamic Method Tests**: Test automatic method generation and functionality
- **Validation Tests**: Test name validation and error handling
- **Exception Tests**: Test custom exceptions for various error conditions

### Edge Cases

Tests cover edge cases and error conditions:

- Invalid statistic names
- Duplicate names across types
- Accessing non-existent statistics
- Type validation for values
- Boundary conditions for numeric values

### Integration Tests

Tests verify that components work together correctly:

- Mixed statistic types in same instance
- Dynamic method generation across all types
- Label management across statistics
- Bulk operations and queries

## Test Coverage

Current test coverage: **100%**

Coverage includes:
- All public methods
- All private helper methods
- Error handling paths
- Edge cases
- Type validation

## Writing Tests

### Test Structure

```python
import pytest
from prostata import Stats

class TestStats:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.stats = Stats()

    def test_set_timer_basic(self):
        """Test basic timer creation."""
        self.stats.set_timer("test_timer")

        # Assert timer exists
        assert self.stats.has_timer("test_timer")

        # Assert dynamic method exists
        assert hasattr(self.stats, "get_test_timer")

    def test_timer_start_stop(self):
        """Test timer start and stop functionality."""
        self.stats.set_timer("response_time")

        # Start timer
        self.stats.start_response_time()

        # Simulate some work
        import time
        time.sleep(0.01)

        # Stop timer
        duration = self.stats.stop_response_time()

        # Assert duration is positive
        assert duration > 0

        # Assert duration is reasonable (less than 1 second)
        assert duration < 1.0
```

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names that explain what is being tested

### Assertions

Use appropriate assertions for different scenarios:

```python
# Equality
assert result == expected

# Identity
assert result is expected

# Truthiness
assert result
assert not result

# Exceptions
with pytest.raises(ValueError):
    invalid_operation()

# Approximate values (for timing)
assert abs(actual - expected) < tolerance

# Collections
assert item in collection
assert len(collection) == expected_length
```

### Fixtures

Use pytest fixtures for reusable test setup:

```python
@pytest.fixture
def stats_instance():
    """Provide a fresh Stats instance for each test."""
    return Stats()

@pytest.fixture
def populated_stats(stats_instance):
    """Provide a Stats instance with some predefined statistics."""
    stats_instance.set_timer("timer1")
    stats_instance.set_counter("counter1", 0)
    stats_instance.set_ratio("ratio1", 0.0)
    stats_instance.set_attribute("attr1", "value")
    return stats_instance

def test_something(populated_stats):
    # Test using the populated stats instance
    assert populated_stats.has_timer("timer1")
```

## Continuous Integration

Tests run automatically on:

- **GitHub Actions**: On every push and pull request
- **Multiple Python versions**: 3.8, 3.9, 3.10, 3.11
- **Multiple operating systems**: Ubuntu, macOS, Windows

### CI Configuration

See `.github/workflows/test.yml` for the complete CI setup.

## Test Dependencies

Development dependencies include:

- `pytest`: Test framework
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking utilities (if needed)

Install with:

```bash
pip install -e ".[dev]"
```

## Debugging Tests

### Running Failed Tests

```bash
# Run only failed tests
pytest --lf

# Run failed tests with detailed output
pytest --lf -v

# Run failed tests and stop on first failure
pytest --lf -x
```

### Debugging with PDB

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb
```

### Verbose Output

```bash
# Show all output
pytest -s

# Show captured output for failed tests
pytest -rN
```

## Performance Testing

For performance-critical code, consider adding benchmarks:

```python
import time

def test_timer_performance(benchmark):
    """Test timer performance under load."""
    stats = Stats()
    stats.set_timer("perf_timer")

    def run_timer():
        stats.start_perf_timer()
        # Simulate work
        time.sleep(0.001)
        stats.stop_perf_timer()

    # Benchmark the operation
    benchmark(run_timer)
```

## Best Practices

### Test Isolation

- Each test should be independent
- Use `setup_method`/`teardown_method` for test isolation
- Don't rely on test execution order

### Test Readability

- Use descriptive test names
- Keep tests focused on one behavior
- Use comments to explain complex test logic
- Follow AAA pattern: Arrange, Act, Assert

### Test Maintenance

- Update tests when changing APIs
- Remove obsolete tests
- Keep test code clean and maintainable
- Review test coverage regularly

### Test Performance

- Keep tests fast (target < 100ms per test)
- Use fixtures for expensive setup
- Parallelize tests when possible
- Mock external dependencies