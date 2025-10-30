"""
Tests for my_package core functionality.
"""
import unittest
from unittest.mock import patch
import io
import sys

from my_package.main import some_function, run_application


class TestMyPackage(unittest.TestCase):
    """Test cases for my_package core functions."""

    def test_some_function(self):
        """Test the greeting function returns expected string."""
        self.assertEqual(some_function(), "Hello, World!")

    def test_run_application_default(self):
        """Test run_application prints default greeting."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            run_application()
            self.assertEqual(fake_out.getvalue().strip(), "Hello, World!")

    def test_run_application_with_option(self):
        """Test run_application prints custom option."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            run_application("Custom message")
            self.assertEqual(fake_out.getvalue().strip(),
                             "Option: Custom message")


if __name__ == '__main__':
    unittest.main()
