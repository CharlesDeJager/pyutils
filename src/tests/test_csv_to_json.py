"""
Tests for CSV to JSON converter functionality.
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

from file_converter.converters.csv_to_json import convert_csv_to_json


class TestCsvToJson(unittest.TestCase):
    """Test cases for CSV to JSON conversion including edge cases and error conditions."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_csv_file = Path(self.test_dir) / "test.csv"
        self.test_json_file = Path(self.test_dir) / "test.json"
        self.maxDiff = None  # Show full diffs in test output

    def tearDown(self):
        """Clean up test files."""
        for file in [self.test_csv_file, self.test_json_file]:
            try:
                file.unlink()
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.test_dir)
        except OSError:
            pass

    def test_basic_conversion(self):
        """Test basic CSV to JSON conversion with default delimiter."""
        test_data = "name,age,city\nAlice,30,New York\nBob,25,Seattle"
        expected = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"}
        ]

        self.test_csv_file.write_text(test_data, encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))

        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, expected)

    def test_custom_delimiters(self):
        """Test CSV conversion with various delimiters."""
        test_cases = [
            ('|', 'name|age|city\nAlice|30|New York\nBob|25|Seattle'),
            ('\t', 'name\tage\tcity\nAlice\t30\tNew York\nBob\t25\tSeattle'),
            (';', 'name;age;city\nAlice;30;New York\nBob;25;Seattle')
        ]

        expected = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"}
        ]

        for delimiter, data in test_cases:
            with self.subTest(delimiter=delimiter):
                self.test_csv_file.write_text(data, encoding='utf-8')
                convert_csv_to_json(
                    str(self.test_csv_file),
                    str(self.test_json_file),
                    delimiter=delimiter
                )
                result = json.loads(
                    self.test_json_file.read_text(encoding='utf-8'))
                self.assertEqual(result, expected)

    def test_type_coercion(self):
        """Test numeric type coercion in CSV values."""
        test_data = (
            "string,int,float,empty,mixed\n"
            "text,42,-123,,'123.45'\n"
            "more,0,3.14,,text\n"
        )

        expected = [
            {
                "string": "text",
                "int": 42,
                "float": -123,
                "empty": "",
                "mixed": "123.45"
            },
            {
                "string": "more",
                "int": 0,
                "float": 3.14,
                "empty": "",
                "mixed": "text"
            }
        ]

        self.test_csv_file.write_text(test_data, encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))

        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, expected)

    def test_complex_data(self):
        """Test handling of complex data types and special characters."""
        test_data = (
            'string,list,dict,boolean,null,special\n'
            '"normal text","[1,2,3]","{""key"":""value""}",true,,"text with, comma"\n'
            '"unicode © ™","[]","{}", false,NULL,"line\\nbreak"\n'
        )
        expected = [
            {
                "string": "normal text",
                "list": "[1,2,3]",
                "dict": '{"key":"value"}',
                "boolean": "true",
                "null": "",
                "special": "text with, comma"
            },
            {
                "string": "unicode © ™",
                "list": "[]",
                "dict": "{}",
                "boolean": "false",
                "null": "NULL",
                "special": "line\\nbreak"
            }
        ]

        self.test_csv_file.write_text(test_data, encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))

        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, expected)

    def test_numeric_edge_cases(self):
        """Test handling of various numeric formats."""
        test_data = (
            "value,type\n"
            "42,integer\n"
            "-42,negative\n"
            "3.14159,float\n"
            "-3.14159,negative float\n"
            "1.23e4,scientific\n"
            "-1.23e-4,negative scientific\n"
            "0xFF,hex\n"
            "0o777,octal\n"
            "0b1010,binary\n"
            "12_345,underscore\n"
            ".5,leading dot\n"
            "+123,plus sign\n"
            "NaN,not a number\n"
            "Infinity,infinity\n"
        )

        self.test_csv_file.write_text(test_data, encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))

        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))

        # Verify specific numeric conversions
        self.assertEqual(result[0]["value"], 42)  # integer
        self.assertEqual(result[1]["value"], -42)  # negative
        self.assertEqual(result[2]["value"], 3.14159)  # float
        self.assertEqual(result[3]["value"], -3.14159)  # negative float
        self.assertEqual(result[4]["value"], 12300)  # scientific
        self.assertEqual(result[5]["value"], -0.000123)  # negative scientific
        self.assertEqual(result[6]["value"], "0xFF")  # hex stays as string
        self.assertEqual(result[7]["value"], "0o777")  # octal stays as string
        # binary stays as string
        self.assertEqual(result[8]["value"], "0b1010")
        self.assertEqual(result[9]["value"], 12345)  # underscore removed
        self.assertEqual(result[10]["value"], 0.5)  # leading dot parsed
        self.assertEqual(result[11]["value"], 123)  # plus sign handled
        self.assertEqual(result[12]["value"], "NaN")  # NaN stays as string
        # Infinity stays as string
        self.assertEqual(result[13]["value"], "Infinity")

    def test_error_handling(self):
        """Test error handling for invalid inputs and edge cases."""
        # Non-existent file
        with self.assertRaises(FileNotFoundError):
            convert_csv_to_json("nonexistent.csv", str(self.test_json_file))

        # Empty file
        self.test_csv_file.write_text("", encoding='utf-8')
        with self.assertRaises(ValueError) as ctx:
            convert_csv_to_json(str(self.test_csv_file),
                                str(self.test_json_file))
        self.assertIn("no headers", str(ctx.exception).lower())

        # Headers only
        self.test_csv_file.write_text("name,age,city", encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))
        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, [])

        # Invalid CSV format
        self.test_csv_file.write_text(
            "name,age\nAlice,25,extra", encoding='utf-8')
        with self.assertRaises(ValueError) as ctx:
            convert_csv_to_json(str(self.test_csv_file),
                                str(self.test_json_file))
        self.assertIn("format", str(ctx.exception).lower())

        # File with only newlines
        self.test_csv_file.write_text("\n\n\n", encoding='utf-8')
        with self.assertRaises(ValueError):
            convert_csv_to_json(str(self.test_csv_file),
                                str(self.test_json_file))

        # Invalid output path
        self.test_csv_file.write_text("name\nAlice", encoding='utf-8')
        with self.assertRaises(IOError):
            convert_csv_to_json(str(self.test_csv_file),
                                "/nonexistent/dir/file.json")

    def test_whitespace_handling(self):
        """Test handling of various whitespace scenarios."""
        test_data = (
            '  name  ,  age  ,  city  \n'
            '  Alice  ,  30  ,  New York  \n'
            '    Bob    ,   25   ,   Seattle    \n'
            '\tCharlie\t,\t35\t,\tChicago\t\n'
        )
        expected = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Seattle"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]

        self.test_csv_file.write_text(test_data, encoding='utf-8')
        convert_csv_to_json(str(self.test_csv_file), str(self.test_json_file))

        result = json.loads(self.test_json_file.read_text(encoding='utf-8'))
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
