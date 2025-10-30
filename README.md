# Python Utilities

A collection of Python command-line utilities for common file operations and data conversions.

## Features

### File Converter

Convert between different file formats with automatic type inference and proper encoding handling.

Currently supported conversions:
- CSV to JSON (with numeric type coercion)
- JSON to CSV (with proper escaping and consistent field handling)

#### CSV to JSON Features

- Automatic type inference for numeric values
- Support for custom delimiters and escape characters
- Proper handling of Unicode and special characters
- Robust error handling and validation

#### JSON to CSV Features

- Support for arrays of objects and single objects
- Consistent field ordering
- Custom delimiters and escape characters
- Proper handling of nested structures
- Empty input handling

## Installation

Install the package in development mode:

```bash
# Clone the repository
git clone https://github.com/yourusername/pyutils.git
cd pyutils

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .
```

## Usage

### File Converter CLI

The file converter utility provides a command-line interface for format conversions:

```bash
# Convert CSV to JSON
file-converter csv-to-json input.csv output.json [options]

# Convert JSON to CSV
file-converter json-to-csv input.json output.csv [options]
```

Options:
- `--delimiter`: Specify custom delimiter (default: ',')
- `--escape`: Specify escape character for special values

Examples:

```bash
# Basic CSV to JSON conversion
file-converter csv-to-json data.csv output.json

# CSV to JSON with custom delimiter
file-converter csv-to-json data.csv output.json --delimiter ';'

# JSON to CSV with custom delimiter and escape char
file-converter json-to-csv data.json output.csv --delimiter ';' --escape '\\'
```

### Python API

You can also use the converters directly in your Python code:

```python
from file_converter.converters.csv_to_json import convert_csv_to_json
from file_converter.converters.json_to_csv import convert_json_to_csv

# Convert CSV to JSON with type inference
convert_csv_to_json(
    csv_file_path='input.csv',
    json_file_path='output.json',
    delimiter=',',
    escape_char='\\'
)

# Convert JSON to CSV
convert_json_to_csv(
    json_file='input.json',
    csv_file='output.csv',
    delimiter=',',
    escape_char='\\'
)
```

## Input Format Examples

### CSV to JSON

Input CSV:
```csv
name,age,salary,city
Alice,30,75000.50,New York
Bob,25,65000.00,Seattle
```

Output JSON:
```json
[
    {
        "name": "Alice",
        "age": 30,
        "salary": 75000.50,
        "city": "New York"
    },
    {
        "name": "Bob",
        "age": 25,
        "salary": 65000.00,
        "city": "Seattle"
    }
]
```

### JSON to CSV

Input JSON:
```json
[
    {
        "name": "Alice",
        "details": {
            "age": 30,
            "city": "New York"
        },
        "skills": ["Python", "SQL"]
    },
    {
        "name": "Bob",
        "details": {
            "age": 25,
            "city": "Seattle"
        },
        "skills": ["Java", "JavaScript"]
    }
]
```

Output CSV:
```csv
name,details,skills
Alice,"{""age"": 30, ""city"": ""New York""}","[""Python"", ""SQL""]"
Bob,"{""age"": 25, ""city"": ""Seattle""}","[""Java"", ""JavaScript""]"
```

## Development

### Running Tests

```bash
# Set Python path to include src directory
set PYTHONPATH=src  # Windows
export PYTHONPATH=src  # Linux/Mac

# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Adding New Features

1. Create new converter modules in `src/file_converter/converters/`
2. Add CLI commands in `src/file_converter/cli.py`
3. Add comprehensive tests in `tests/`
4. Update documentation in docstrings and README.md

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.