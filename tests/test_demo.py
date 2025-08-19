"""
Tests for the demo module.

This module demonstrates testing with pytest and Python 3.10+ features.
"""

import pytest
from your_project_name.demo import greet, process_data, calculate_stats


class TestGreet:
    """Test cases for the greet function."""
    
    def test_greet_with_default_greeting(self):
        """Test greeting with default message."""
        result = greet("Alice")
        assert result == "Hello, Alice!"
    
    def test_greet_with_custom_greeting(self):
        """Test greeting with custom message."""
        result = greet("Bob", "Good morning")
        assert result == "Good morning, Bob!"
    
    def test_greet_with_empty_name(self):
        """Test greeting with empty name."""
        result = greet("")
        assert result == "Hello, !"
    
    def test_greet_with_none_greeting(self):
        """Test greeting with None greeting (should use default)."""
        result = greet("Charlie", None)
        assert result == "Hello, Charlie!"


class TestProcessData:
    """Test cases for the process_data function."""
    
    def test_process_string_data(self):
        """Test processing string data."""
        result = process_data("hello")
        assert result == "String: hello"
    
    def test_process_list_data(self):
        """Test processing list data."""
        result = process_data(["a", "b", "c"])
        assert result == "List with 3 items: a, b, c"
    
    def test_process_empty_list(self):
        """Test processing empty list."""
        result = process_data([])
        assert result == "List with 0 items: "
    
    def test_process_dict_data(self):
        """Test processing dictionary data."""
        result = process_data({"name": "Alice", "age": 30})
        assert result == "Dictionary with keys: name, age"
    
    def test_process_empty_dict(self):
        """Test processing empty dictionary."""
        result = process_data({})
        assert result == "Dictionary with keys: "
    
    def test_process_none_data(self):
        """Test processing None data."""
        result = process_data(None)
        assert result == "Unknown type: NoneType"
    
    def test_process_int_data(self):
        """Test processing integer data."""
        result = process_data(42)
        assert result == "Unknown type: int"


class TestCalculateStats:
    """Test cases for the calculate_stats function."""
    
    def test_calculate_stats_with_numbers(self):
        """Test statistics calculation with valid numbers."""
        numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = calculate_stats(numbers)
        
        expected = {
            "count": 5,
            "sum": 15.0,
            "mean": 3.0,
            "min": 1.0,
            "max": 5.0
        }
        assert result == expected
    
    def test_calculate_stats_with_empty_list(self):
        """Test statistics calculation with empty list."""
        result = calculate_stats([])
        
        expected = {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0
        }
        assert result == expected
    
    def test_calculate_stats_with_single_number(self):
        """Test statistics calculation with single number."""
        result = calculate_stats([42.5])
        
        expected = {
            "count": 1,
            "sum": 42.5,
            "mean": 42.5,
            "min": 42.5,
            "max": 42.5
        }
        assert result == expected
    
    def test_calculate_stats_with_negative_numbers(self):
        """Test statistics calculation with negative numbers."""
        numbers = [-5.0, -2.0, 0.0, 3.0, 7.0]
        result = calculate_stats(numbers)
        
        expected = {
            "count": 5,
            "sum": 3.0,
            "mean": 0.6,
            "min": -5.0,
            "max": 7.0
        }
        assert result == expected
    
    def test_calculate_stats_with_floats(self):
        """Test statistics calculation with floating point numbers."""
        numbers = [1.5, 2.7, 3.2, 4.1, 5.9]
        result = calculate_stats(numbers)
        
        assert result["count"] == 5
        assert result["sum"] == pytest.approx(17.4)
        assert result["mean"] == pytest.approx(3.48)
        assert result["min"] == 1.5
        assert result["max"] == 5.9


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_greet_and_process_integration(self):
        """Test integration between greet and process_data functions."""
        greeting = greet("Test User")
        processed = process_data(greeting)
        
        assert "String: Hello, Test User!" in processed
    
    def test_stats_and_process_integration(self):
        """Test integration between calculate_stats and process_data functions."""
        numbers = [1, 2, 3]
        stats = calculate_stats(numbers)
        processed = process_data(stats)
        
        assert "Dictionary with keys:" in processed
        assert "count" in processed
        assert "sum" in processed
        assert "mean" in processed


# Parametrized tests
@pytest.mark.parametrize("name,greeting,expected", [
    ("Alice", None, "Hello, Alice!"),
    ("Bob", "Hi", "Hi, Bob!"),
    ("Charlie", "Good evening", "Good evening, Charlie!"),
    ("", "Welcome", "Welcome, !"),
])
def test_greet_parametrized(name, greeting, expected):
    """Parametrized test for greet function."""
    result = greet(name, greeting)
    assert result == expected


@pytest.mark.parametrize("numbers,expected_count,expected_sum", [
    ([1, 2, 3], 3, 6.0),
    ([], 0, 0.0),
    ([42], 1, 42.0),
    ([1.5, 2.5], 2, 4.0),
])
def test_calculate_stats_parametrized(numbers, expected_count, expected_sum):
    """Parametrized test for calculate_stats function."""
    result = calculate_stats(numbers)
    assert result["count"] == expected_count
    assert result["sum"] == expected_sum


# Performance tests
@pytest.mark.slow
def test_calculate_stats_performance():
    """Performance test for calculate_stats with large dataset."""
    import time
    
    # Generate large dataset
    numbers = list(range(10000))
    
    start_time = time.time()
    result = calculate_stats(numbers)
    end_time = time.time()
    
    # Should complete within 1 second
    assert end_time - start_time < 1.0
    
    # Verify results
    assert result["count"] == 10000
    assert result["sum"] == 49995000.0
    assert result["mean"] == 4999.5
    assert result["min"] == 0
    assert result["max"] == 9999


# Error handling tests
def test_greet_with_non_string_name():
    """Test greet function with non-string name."""
    with pytest.raises(TypeError):
        greet(123)  # type: ignore


def test_calculate_stats_with_non_numeric_list():
    """Test calculate_stats function with non-numeric list."""
    with pytest.raises(TypeError):
        calculate_stats(["not", "numbers"])  # type: ignore
