"""
Integration tests for file converter utilities.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List, Optional, Tuple

import pytest

from file_converter import cli


class TestFileConverterIntegration(unittest.TestCase):
    """Integration tests for file converter CLI and utilities."""

    def setUp(self):
        """Create temporary directory and files for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.csv_file = Path(self.test_dir) / "test.csv"
        self.json_file = Path(self.test_dir) / "test.json"
        self.maxDiff = None

    def tearDown(self):
        """Clean up test files."""
        for file in [self.csv_file, self.json_file]:
            try:
                file.unlink()
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.test_dir)
        except OSError:
            pass

    def _run_cli(
        self,
        command: str,
        args: List[str],
        input_data: Optional[str] = None
    ) -> Tuple[int, str, str]:
        """
        Run CLI command and return exit code, stdout, and stderr.

        Args:
            command: The subcommand to run (e.g., 'csv-to-json')
            args: List of additional arguments
            input_data: Optional input data to write to input file

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        if input_data is not None:
            if command == 'csv-to-json':
                self.csv_file.write_text(input_data, encoding='utf-8')
            else:
                self.json_file.write_text(input_data, encoding='utf-8')

        # Use subprocess to run the command
        process = subprocess.Popen(
            [sys.executable, '-m', 'file_converter', command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def test_csv_to_json_cli(self):
        """Test CSV to JSON conversion through CLI."""
        csv_data = "name,age,city\nAlice,30,New York\nBob,25,Seattle"
        expected_json = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"}
        ]

        exit_code, stdout, stderr = self._run_cli(
            'csv-to-json',
            [str(self.csv_file), str(self.json_file)],
            csv_data
        )

        self.assertEqual(exit_code, 0)
        self.assertFalse(stderr)
        self.assertTrue(stdout)

        result = json.loads(self.json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, expected_json)

    def test_json_to_csv_cli(self):
        """Test JSON to CSV conversion through CLI."""
        json_data = json.dumps([
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"}
        ])
        expected_csv = "name,age,city\nAlice,30,New York\nBob,25,Seattle\n"

        exit_code, stdout, stderr = self._run_cli(
            'json-to-csv',
            [str(self.json_file), str(self.csv_file)],
            json_data
        )

        self.assertEqual(exit_code, 0)
        self.assertFalse(stderr)
        self.assertTrue(stdout)

        result = self.csv_file.read_text(encoding='utf-8')
        # Normalize line endings for comparison
        result = result.replace('\r\n', '\n')
        self.assertEqual(result, expected_csv)

    def test_cli_error_handling(self):
        """Test CLI error handling for various scenarios."""
        test_cases = [
            # Missing input file
            (
                'csv-to-json',
                ['nonexistent.csv', str(self.json_file)],
                None,
                1,
                'not found'
            ),
            # Invalid JSON
            (
                'json-to-csv',
                [str(self.json_file), str(self.csv_file)],
                '{invalid json',
                1,
                'Invalid JSON'
            ),
            # Empty CSV
            (
                'csv-to-json',
                [str(self.csv_file), str(self.json_file)],
                '',
                1,
                'no headers'
            ),
            # Invalid output path
            (
                'csv-to-json',
                [str(self.csv_file), '/nonexistent/dir/out.json'],
                'name,age\nAlice,30',
                1,
                'Error'
            )
        ]

        for command, args, input_data, expected_code, expected_error in test_cases:
            with self.subTest(command=command, args=args):
                exit_code, stdout, stderr = self._run_cli(
                    command,
                    args,
                    input_data
                )
                self.assertEqual(exit_code, expected_code)
                self.assertTrue(expected_error.lower() in stderr.lower())

    def test_cli_with_options(self):
        """Test CLI with various option combinations."""
        # Test CSV to JSON with custom delimiter
        csv_data = "name;age;city\nAlice;30;New York\nBob;25;Seattle"
        exit_code, stdout, stderr = self._run_cli(
            'csv-to-json',
            [
                str(self.csv_file),
                str(self.json_file),
                '--delimiter',
                ';'
            ],
            csv_data
        )

        self.assertEqual(exit_code, 0)
        result = json.loads(self.json_file.read_text(encoding='utf-8'))
        self.assertEqual(result[0]["age"], 30)
        self.assertEqual(result[1]["city"], "Seattle")

        # Test JSON to CSV with custom delimiter and escape
        json_data = json.dumps([
            {"name": "Alice,Jr", "age": 30},
            {"name": "Bob,Sr", "age": 25}
        ])

        exit_code, stdout, stderr = self._run_cli(
            'json-to-csv',
            [
                str(self.json_file),
                str(self.csv_file),
                '--delimiter',
                ';',
                '--escape',
                '\\'
            ],
            json_data
        )

        self.assertEqual(exit_code, 0)
        result = self.csv_file.read_text(encoding='utf-8')
        self.assertTrue('Alice,Jr' in result)
        self.assertTrue('Bob,Sr' in result)
        self.assertTrue(';' in result)  # Verify custom delimiter

    def test_round_trip_conversion(self):
        """Test round-trip conversion from CSV to JSON and back."""
        original_csv = (
            "name,age,salary,active\n"
            "Alice,30,75000.50,true\n"
            "Bob,25,65000.00,false\n"
        )

        # CSV to JSON
        self._run_cli(
            'csv-to-json',
            [str(self.csv_file), str(self.json_file)],
            original_csv
        )

        # JSON back to CSV
        self._run_cli(
            'json-to-csv',
            [str(self.json_file), str(self.csv_file)]
        )

        # Compare results (normalizing line endings)
        final_csv = self.csv_file.read_text(
            encoding='utf-8').replace('\r\n', '\n')
        original_csv = original_csv.replace('\r\n', '\n')

        # CSV files should match except for boolean values which may be capitalized
        final_csv = final_csv.lower()
        original_csv = original_csv.lower()
        self.assertEqual(final_csv, original_csv)


if __name__ == '__main__':
    pytest.main([__file__])
