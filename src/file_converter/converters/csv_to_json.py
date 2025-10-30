"""
CSV to JSON converter module.

This module provides functionality to convert CSV files to JSON format,
with automatic type inference for numeric values.

Example:
    Basic usage with default settings:
        >>> from file_converter.converters.csv_to_json import convert_csv_to_json
        >>> convert_csv_to_json('input.csv', 'output.json')

    Using custom delimiter and escape character:
        >>> convert_csv_to_json(
        ...     'input.csv',
        ...     'output.json',
        ...     delimiter=';',
        ...     escape_char='\\'
        ... )

Input CSV format:
    name,age,salary
    Alice,30,75000.50
    Bob,25,65000

Output JSON format:
    [
        {
            "name": "Alice",
            "age": 30,
            "salary": 75000.50
        },
        {
            "name": "Bob",
            "age": 25,
            "salary": 65000
        }
    ]

Note:
    - The converter attempts to coerce numeric values to their appropriate types
    - Empty values in CSV will be preserved as empty strings in JSON
    - All files are assumed to be UTF-8 encoded
"""
import csv
import json
from typing import Any, Dict, List, Optional


def convert_csv_to_json(
    csv_file_path: str,
    json_file_path: str,
    delimiter: str = ',',
    escape_char: Optional[str] = '\\'
) -> None:
    """
    Convert a CSV file to JSON. Will attempt to coerce numeric values (ints/floats).

    Args:
        csv_file_path: Path to the input CSV file
        json_file_path: Path to output JSON file
        delimiter: CSV delimiter character (default: ',')
        escape_char: Escape character for CSV (default: '\\')

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If CSV is malformed
        IOError: If there are issues reading/writing files
    """
    def _parse_value(v: Optional[str]) -> Any:
        """Parse string values into appropriate types."""
        if v is None:
            return None
        v = v.strip()
        if v == '':
            return ''

        # Try integer
        if v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
            try:
                return int(v)
            except ValueError:
                pass

        # Try float
        try:
            return float(v)
        except ValueError:
            pass

        return v

    try:
        data: List[Dict[str, Any]] = []

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(
                csv_file,
                delimiter=delimiter,
                escapechar=escape_char
            )
            if not csv_reader.fieldnames:
                raise ValueError("CSV file has no headers")

            for row in csv_reader:
                parsed = {k: _parse_value(v) for k, v in row.items()}
                data.append(parsed)

        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {csv_file_path}")
    except csv.Error as e:
        raise ValueError(f"Invalid CSV format: {str(e)}")
    except Exception as e:
        raise IOError(f"Error converting CSV to JSON: {str(e)}")
