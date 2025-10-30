"""
Tests for JSON to CSV converter functionality.
"""
import csv
import json
import os
import tempfile
import unittest
from pathlib import Path

from file_converter.converters.json_to_csv import convert_json_to_csv


class TestJsonToCsv(unittest.TestCase):
    """Test cases for JSON to CSV conversion including edge cases and special formats."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_json_file = Path(self.test_dir) / "test.json"
        self.test_csv_file = Path(self.test_dir) / "test.csv"
        self.maxDiff = None  # Show full diffs in test output

    def tearDown(self):
        """Clean up test files."""
        for file in [self.test_json_file, self.test_csv_file]:
            try:
                file.unlink()
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.test_dir)
        except OSError:
            pass

    def test_basic_conversion(self):
        """Test basic JSON to CSV conversion."""
        test_data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"}
        ]

        self.test_json_file.write_text(
            json.dumps(test_data),
            encoding='utf-8'
        )

        convert_json_to_csv(str(self.test_json_file), str(self.test_csv_file))

        with open(self.test_csv_file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            result = list(reader)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Alice")
        self.assertEqual(result[0]["age"], "30")
        self.assertEqual(result[1]["city"], "Seattle")

    def test_custom_delimiter(self):
        """Test CSV conversion with custom delimiters."""
        test_data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]

        self.test_json_file.write_text(
            json.dumps(test_data),
            encoding='utf-8'
        )

        for delimiter in [',', ';', '|', '\t']:
            with self.subTest(delimiter=delimiter):
                convert_json_to_csv(
                    str(self.test_json_file),
                    str(self.test_csv_file),
                    delimiter=delimiter
                )

                with open(self.test_csv_file, encoding='utf-8', newline='') as f:
                    content = f.read()
                    self.assertIn(delimiter.join(['name', 'age']), content)

    def test_special_cases(self):
        """Test handling of special cases and edge conditions."""
        test_cases = [
            # Empty array
            ([], []),

            # Single object
            ({"name": "Alice", "age": 30}, [{"name": "Alice", "age": "30"}]),

            # Array with one object
            ([{"name": "Alice", "age": 30}], [{"name": "Alice", "age": "30"}]),

            # Mixed types
            ([
                {"name": "Alice", "age": 30, "active": True},
                {"name": "Bob", "age": 25, "active": False}
            ], [
                {"name": "Alice", "age": "30", "active": "True"},
                {"name": "Bob", "age": "25", "active": "False"}
            ])
        ]

        for input_data, expected in test_cases:
            with self.subTest(input_data=input_data):
                self.test_json_file.write_text(
                    json.dumps(input_data),
                    encoding='utf-8'
                )

                convert_json_to_csv(
                    str(self.test_json_file),
                    str(self.test_csv_file)
                )

                if not input_data:  # Empty case
                    self.assertEqual(
                        self.test_csv_file.read_text(encoding='utf-8'),
                        ''
                    )
                else:
                    with open(self.test_csv_file, encoding='utf-8', newline='') as f:
                        reader = csv.DictReader(f)
                        result = list(reader)
                        self.assertEqual(result, expected)

    def test_complex_data_types(self):
        """Test conversion of complex JSON data types."""
        test_data = [
            {
                "null": None,
                "bool": True,
                "int": 42,
                "float": 3.14,
                "string": "text",
                "array": [1, 2, 3],
                "object": {"key": "value"},
                "special": "with,comma"
            },
            {
                "null": None,
                "bool": False,
                "int": -42,
                "float": -3.14,
                "string": "more text",
                "array": [],
                "object": {},
                "special": "with\nlinebreak"
            }
        ]

        expected_csv_data = [
            {
                "null": "",
                "bool": "True",
                "int": "42",
                "float": "3.14",
                "string": "text",
                "array": "[1, 2, 3]",
                "object": '{"key": "value"}',
                "special": "with,comma"
            },
            {
                "null": "",
                "bool": "False",
                "int": "-42",
                "float": "-3.14",
                "string": "more text",
                "array": "[]",
                "object": "{}",
                "special": "with\nlinebreak"
            }
        ]

        self.test_json_file.write_text(json.dumps(test_data), encoding='utf-8')
        convert_json_to_csv(str(self.test_json_file), str(self.test_csv_file))

        with open(self.test_csv_file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            result = list(reader)
            self.assertEqual(result, expected_csv_data)

    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        test_data = [
            {
                "symbols": "©®™",
                "emoji": "😀🌟🌍",
                "chinese": "你好",
                "arabic": "مرحبا",
                "russian": "привет",
                "accents": "éèêë"
            }
        ]

        self.test_json_file.write_text(json.dumps(test_data), encoding='utf-8')
        convert_json_to_csv(str(self.test_json_file), str(self.test_csv_file))

        with open(self.test_csv_file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            result = list(reader)[0]

            self.assertEqual(result["symbols"], "©®™")
            self.assertEqual(result["emoji"], "😀🌟🌍")
            self.assertEqual(result["chinese"], "你好")
            self.assertEqual(result["arabic"], "مرحبا")
            self.assertEqual(result["russian"], "привет")
            self.assertEqual(result["accents"], "éèêë")

    def test_nested_structures(self):
        """Test handling of deeply nested JSON structures."""
        test_data = [
            {
                "id": 1,
                "nested_array": [
                    [1, 2],
                    {"a": "b"},
                    [{"x": "y"}]
                ],
                "nested_object": {
                    "level1": {
                        "level2": {
                            "level3": "value"
                        }
                    }
                }
            }
        ]

        self.test_json_file.write_text(json.dumps(test_data), encoding='utf-8')
        convert_json_to_csv(str(self.test_json_file), str(self.test_csv_file))

        with open(self.test_csv_file, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            result = list(reader)[0]

            self.assertEqual(result["id"], "1")
            self.assertEqual(
                json.loads(result["nested_array"]),
                [[1, 2], {"a": "b"}, [{"x": "y"}]]
            )
            self.assertEqual(
                json.loads(result["nested_object"]),
                {"level1": {"level2": {"level3": "value"}}}
            )

    def test_error_handling(self):
        """Test error handling for invalid inputs and edge cases."""
        # Invalid JSON syntax
        invalid_json_cases = [
            "{invalid json",
            "[1, 2, 3",
            '{"missing": "quote}',
            "{'wrong': 'quotes'}",
            "[null, undefined]"  # undefined is not valid JSON
        ]

        for invalid_json in invalid_json_cases:
            with self.subTest(invalid_json=invalid_json):
                self.test_json_file.write_text(invalid_json, encoding='utf-8')
                with self.assertRaises(ValueError) as ctx:
                    convert_json_to_csv(
                        str(self.test_json_file),
                        str(self.test_csv_file)
                    )
                self.assertIn("json", str(ctx.exception).lower())

        # Non-existent input file
        with self.assertRaises(FileNotFoundError) as ctx:
            convert_json_to_csv(
                "nonexistent.json",
                str(self.test_csv_file)
            )
        self.assertIn("not found", str(ctx.exception).lower())

        # Invalid input types
        invalid_types = [
            "42",  # number
            '"string"',  # string
            "true",  # boolean
            "null",  # null
            "[1,2,3]"  # array of non-objects
        ]

        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                self.test_json_file.write_text(invalid_type, encoding='utf-8')
                with self.assertRaises(ValueError) as ctx:
                    convert_json_to_csv(
                        str(self.test_json_file),
                        str(self.test_csv_file)
                    )
                self.assertIn("must contain", str(ctx.exception).lower())

        # Inconsistent object structures
        inconsistent_data = [
            {"a": 1, "b": 2},
            {"a": 1, "c": 3},  # 'b' missing, 'c' added
            {"a": 1, "b": 2, "d": 4}  # extra field 'd'
        ]

        self.test_json_file.write_text(
            json.dumps(inconsistent_data), encoding='utf-8')
        with self.assertRaises(ValueError) as ctx:
            convert_json_to_csv(str(self.test_json_file),
                                str(self.test_csv_file))
        self.assertIn("same fields", str(ctx.exception).lower())

        # Invalid output path
        self.test_json_file.write_text(
            json.dumps([{"a": 1}]), encoding='utf-8')
        with self.assertRaises(IOError):
            convert_json_to_csv(
                str(self.test_json_file),
                "/nonexistent/dir/file.csv"
            )


if __name__ == '__main__':
    unittest.main()
