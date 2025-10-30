"""
JSON to CSV converter module.

This module provides functionality to convert JSON files containing arrays of
objects into CSV format. It handles both single objects and arrays of objects,
ensuring consistent field names across all records.

Example:
    Basic usage with default settings:
        >>> from file_converter.converters.json_to_csv import convert_json_to_csv
        >>> convert_json_to_csv('input.json', 'output.csv')

    Using custom delimiter and escape character:
        >>> convert_json_to_csv(
        ...     'input.json',
        ...     'output.csv',
        ...     delimiter=';',
        ...     escape_char='\\'
        ... )

Input JSON format:
    [
        {
            "name": "Alice",
            "age": 30,
            "city": "New York"
        },
        {
            "name": "Bob",
            "age": 25,
            "city": "Seattle"
        }
    ]

Output CSV format:
    name,age,city
    Alice,30,New York
    Bob,25,Seattle

Note:
    - All objects in the JSON array must have the same field names
    - Single objects are automatically converted to single-row CSVs
    - Empty arrays produce empty CSV files
    - All files are assumed to be UTF-8 encoded
    - Boolean and numeric values are converted to strings
"""
import csv
import json
from typing import Any, Dict, List, Optional, Union


def convert_json_to_csv(
    json_file: str,
    csv_file: str,
    delimiter: str = ',',
    escape_char: Optional[str] = None
) -> None:
    """
    Convert a JSON array-of-objects file to CSV.

    Args:
        json_file: Path to input JSON file
        csv_file: Path to output CSV file
        delimiter: CSV delimiter character (default: ',')
        escape_char: Optional escape character for CSV values

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If JSON is invalid or empty
        IOError: If there are issues reading/writing files
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as jf:
            data = json.load(jf)

        # Handle single object case
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON must contain an object or array of objects")

        # Handle empty input case
        if not data:
            with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
                cf.write('')
            return

        fieldnames = list(data[0].keys())

        # Validate all objects have the same structure
        for item in data[1:]:
            if set(item.keys()) != set(fieldnames):
                raise ValueError(
                    "All objects in JSON array must have the same fields")

        with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
            writer = csv.DictWriter(
                cf,
                fieldnames=fieldnames,
                delimiter=delimiter,
                escapechar=escape_char
            )
            writer.writeheader()
            writer.writerows(data)

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {json_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise IOError(f"Error converting JSON to CSV: {str(e)}")
