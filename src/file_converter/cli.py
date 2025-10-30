"""
Command-line interface for file format converter utilities.
"""
import argparse
import os
import sys
from typing import Optional

from file_converter.converters.csv_to_json import convert_csv_to_json
from file_converter.converters.json_to_csv import convert_json_to_csv


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='File format converter CLI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # CSV to JSON converter
    csv_to_json_parser = subparsers.add_parser(
        'csv-to-json',
        help='Convert CSV to JSON',
        description='Convert a CSV file to JSON format with type inference'
    )
    csv_to_json_parser.add_argument(
        'input_file',
        help='Input CSV file path'
    )
    csv_to_json_parser.add_argument(
        'output_file',
        help='Output JSON file path'
    )
    csv_to_json_parser.add_argument(
        '--delimiter',
        default=',',
        help='CSV delimiter character'
    )
    csv_to_json_parser.add_argument(
        '--escape',
        default='\\',
        help='Escape character for CSV'
    )

    # JSON to CSV converter
    json_to_csv_parser = subparsers.add_parser(
        'json-to-csv',
        help='Convert JSON to CSV',
        description='Convert a JSON array of objects to CSV format'
    )
    json_to_csv_parser.add_argument(
        'input_file',
        help='Input JSON file path'
    )
    json_to_csv_parser.add_argument(
        'output_file',
        help='Output CSV file path'
    )
    json_to_csv_parser.add_argument(
        '--delimiter',
        default=',',
        help='CSV delimiter character'
    )
    json_to_csv_parser.add_argument(
        '--escape',
        help='Escape character for CSV'
    )

    args = parser.parse_args()

    try:
        if not os.path.isfile(args.input_file):
            raise FileNotFoundError(f"Input file not found: {args.input_file}")

        if os.path.exists(args.output_file):
            print(
                f"Warning: Output file {args.output_file} already exists and will be overwritten.")

        if args.command == 'csv-to-json':
            convert_csv_to_json(
                args.input_file,
                args.output_file,
                args.delimiter,
                args.escape
            )
        else:  # json-to-csv
            convert_json_to_csv(
                args.input_file,
                args.output_file,
                args.delimiter,
                args.escape
            )

        print(
            f"Successfully converted {args.input_file} to {args.output_file}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"Error: An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
