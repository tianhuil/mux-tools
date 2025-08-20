"""
Tests for the demo module.

This module demonstrates testing with pytest and Python 3.10+ features.
"""

from _demo import greet


class TestGreet:
    """Test cases for the greet function."""
    
    def test_greet_with_default_greeting(self) -> None:
        """Test greeting with default message."""
        result = greet("Alice")
        assert result == "Hello, Alice!"
    
    def test_greet_with_custom_greeting(self) -> None:
        """Test greeting with custom message."""
        result = greet("Bob", "Good morning")
        assert result == "Good morning, Bob!"
    
    def test_greet_with_empty_name(self) -> None:
        """Test greeting with empty name."""
        result = greet("")
        assert result == "Hello, !"
    
    def test_greet_with_none_greeting(self)-> None:
        """Test greeting with None greeting (should use default)."""
        result = greet("Charlie", None)
        assert result == "Hello, Charlie!"
