"""
Demo module for your project.

This module demonstrates Python 3.10+ features and provides the main functionality.
"""

from typing import Any, Dict, List, Optional, Union
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def greet(name: str, greeting: Optional[str] = None) -> str:
    """
    Greet someone with a customizable message.
    
    Args:
        name: The name of the person to greet
        greeting: Optional custom greeting message
        
    Returns:
        A greeting string
        
    Example:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob", "Good morning")
        'Good morning, Bob!'
    """
    if greeting is None:
        greeting = "Hello"
    
    return f"{greeting}, {name}!"


def process_data(data: Union[str, List[str], Dict[str, Any]]) -> str:
    """
    Process different types of data using Python 3.10+ pattern matching.
    
    Args:
        data: Data to process (string, list, or dict)
        
    Returns:
        Processed data as string
        
    Example:
        >>> process_data("hello")
        'String: hello'
        >>> process_data(["a", "b", "c"])
        'List with 3 items: a, b, c'
        >>> process_data({"name": "Alice", "age": 30})
        'Dictionary with keys: name, age'
    """
    match data:
        case str():
            return f"String: {data}"
        case list() as items:
            return f"List with {len(items)} items: {', '.join(str(item) for item in items)}"
        case dict() as d:
            keys = ', '.join(d.keys())
            return f"Dictionary with keys: {keys}"
        case _:
            return f"Unknown type: {type(data).__name__}"


def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """
    Calculate basic statistics for a list of numbers.
    
    Args:
        numbers: List of numbers to analyze
        
    Returns:
        Dictionary containing count, sum, mean, min, and max
        
    Example:
        >>> calculate_stats([1, 2, 3, 4, 5])
        {'count': 5, 'sum': 15.0, 'mean': 3.0, 'min': 1.0, 'max': 5.0}
    """
    if not numbers:
        return {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0
        }
    
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    
    return {
        "count": count,
        "sum": total,
        "mean": mean,
        "min": min(numbers),
        "max": max(numbers)
    }


def main() -> None:
    """Main function demonstrating the package functionality."""
    logger.info("Starting your project...")
    
    # Demonstrate greeting function
    print(greet("World"))
    print(greet("Developer", "Welcome"))
    
    # Demonstrate pattern matching
    print(process_data("hello"))
    print(process_data(["apple", "banana", "cherry"]))
    print(process_data({"language": "Python", "version": "3.10"}))
    
    # Demonstrate statistics
    numbers = [1.5, 2.7, 3.2, 4.1, 5.9]
    stats = calculate_stats(numbers)
    print(f"Statistics: {stats}")
    
    logger.info("Your project completed successfully!")


# CLI wrapper functions for script entry points
def greet_cli() -> int:
    """
    CLI wrapper for the greet function.
    
    This function is referenced in pyproject.toml under [project.scripts]
    as "wt-greet = 'wt_tools.demo:greet_cli'"
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Greet someone')
    parser.add_argument('name', help='Name to greet')
    parser.add_argument('--greeting', '-g', help='Custom greeting message')
    
    args = parser.parse_args()
    
    try:
        result = greet(args.name, args.greeting)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def stats_cli() -> int:
    """
    CLI wrapper for the calculate_stats function.
    
    This function is referenced in pyproject.toml under [project.scripts]
    as "wt-stats = 'wt_tools.demo:stats_cli'"
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Calculate statistics for numbers')
    parser.add_argument('numbers', nargs='+', type=float, help='Numbers to analyze')
    
    args = parser.parse_args()
    
    try:
        result = calculate_stats(args.numbers)
        print("Statistics:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()
