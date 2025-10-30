"""
Command-line interface for file format converter utilities.
"""
import argparse
import glob
import os
import sys
from typing import Optional, List, Tuple
from pathlib import Path

from file_converter.converters.csv_to_json import convert_csv_to_json
from file_converter.converters.json_to_csv import convert_json_to_csv


def process_bulk_conversion(command: str, input_pattern: str, output_dir: str, delimiter: str, escape: str) -> None:
    """
    Process bulk file conversion based on input pattern.

    Args:
        command: The conversion command (csv-to-json or json-to-csv)
        input_pattern: Glob pattern for input files
        output_dir: Directory for output files
        delimiter: CSV delimiter character
        escape: Escape character for CSV
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of input files
    input_files = glob.glob(input_pattern, recursive=True)
    if not input_files:
        raise ValueError(f"No files found matching pattern: {input_pattern}")

    total_files = len(input_files)
    print(f"Found {total_files} files to convert")

    # Process each file
    for idx, input_file in enumerate(input_files, 1):
        # Generate output filename
        input_path = Path(input_file)
        output_ext = ".json" if command == "csv-to-json" else ".csv"
        output_file = Path(output_dir) / (input_path.stem + output_ext)

        print(f"[{idx}/{total_files}] Converting {input_file} to {output_file}")

        try:
            if command == "csv-to-json":
                convert_csv_to_json(input_file, str(
                    output_file), delimiter, escape)
            else:  # json-to-csv
                convert_json_to_csv(input_file, str(
                    output_file), delimiter, escape)
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}", file=sys.stderr)
            continue

    print(f"\nBulk conversion complete. Processed {total_files} files.")


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
        description='Convert CSV files to JSON format with type inference'
    )
    csv_input_group = csv_to_json_parser.add_mutually_exclusive_group(
        required=True)
    csv_input_group.add_argument(
        '--file',
        help='Single input CSV file path'
    )
    csv_input_group.add_argument(
        '--pattern',
        help='Glob pattern for bulk CSV file conversion (e.g., "data/*.csv")'
    )

    csv_output_group = csv_to_json_parser.add_mutually_exclusive_group(
        required=True)
    csv_output_group.add_argument(
        '--output-file',
        help='Output JSON file path (for single file conversion)'
    )
    csv_output_group.add_argument(
        '--output-dir',
        help='Output directory for bulk conversion'
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
        description='Convert JSON array files to CSV format'
    )
    json_input_group = json_to_csv_parser.add_mutually_exclusive_group(
        required=True)
    json_input_group.add_argument(
        '--file',
        help='Single input JSON file path'
    )
    json_input_group.add_argument(
        '--pattern',
        help='Glob pattern for bulk JSON file conversion (e.g., "data/*.json")'
    )

    json_output_group = json_to_csv_parser.add_mutually_exclusive_group(
        required=True)
    json_output_group.add_argument(
        '--output-file',
        help='Output CSV file path (for single file conversion)'
    )
    json_output_group.add_argument(
        '--output-dir',
        help='Output directory for bulk conversion'
    )

    json_to_csv_parser.add_argument(
        '--delimiter',
        default=',',
        help='CSV delimiter character'
    )
    json_to_csv_parser.add_argument(
        '--escape',
        default='\\',
        help='Escape character for CSV'
    )

    args = parser.parse_args()

    try:
        if args.pattern:
            # Bulk conversion mode
            process_bulk_conversion(
                args.command,
                args.pattern,
                args.output_dir,
                args.delimiter,
                args.escape
            )
        else:
            # Single file conversion mode
            if not os.path.isfile(args.file):
                raise FileNotFoundError(f"Input file not found: {args.file}")

            if os.path.exists(args.output_file):
                print(
                    f"Warning: Output file {args.output_file} already exists and will be overwritten.")

            if args.command == 'csv-to-json':
                convert_csv_to_json(
                    args.file,
                    args.output_file,
                    args.delimiter,
                    args.escape
                )
            else:  # json-to-csv
                convert_json_to_csv(
                    args.file,
                    args.output_file,
                    args.delimiter,
                    args.escape
                )

            print(f"Successfully converted {args.file} to {args.output_file}")

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
