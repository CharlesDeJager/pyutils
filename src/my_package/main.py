"""
Core functionality for my_package.
"""
from typing import Optional


def some_function() -> str:
    """Example utility function that returns a greeting."""
    return "Hello, World!"


def run_application(option: Optional[str] = None) -> None:
    """
    Main application runner that prints either a greeting or custom option.

    Args:
        option: Optional custom message to print
    """
    if option:
        print(f"Option: {option}")
    else:
        print(some_function())


if __name__ == "__main__":
    run_application()
