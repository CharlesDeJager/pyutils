import argparse
import sys
from file_converter.converters.csv_to_json import convert_csv_to_json
from file_converter.converters.json_to_csv import convert_json_to_csv

def main():
    parser = argparse.ArgumentParser(description="File format converter CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for CSV to JSON
    csv_to_json_parser = subparsers.add_parser('csv-to-json', help='Convert CSV to JSON')
    csv_to_json_parser.add_argument('input_file', help='Input CSV file path')
    csv_to_json_parser.add_argument('output_file', help='Output JSON file path')
    csv_to_json_parser.add_argument('--delimiter', default=',', help='CSV delimiter (default: ",")')
    csv_to_json_parser.add_argument('--escape', default=None, help='Escape character for CSV')

    # Subparser for JSON to CSV
    json_to_csv_parser = subparsers.add_parser('json-to-csv', help='Convert JSON to CSV')
    json_to_csv_parser.add_argument('input_file', help='Input JSON file path')
    json_to_csv_parser.add_argument('output_file', help='Output CSV file path')
    json_to_csv_parser.add_argument('--delimiter', default=',', help='CSV delimiter (default: ",")')
    json_to_csv_parser.add_argument('--escape', default=None, help='Escape character for CSV')

    args = parser.parse_args()

    if args.command == 'csv-to-json':
        convert_csv_to_json(args.input_file, args.output_file, args.delimiter, args.escape)
    elif args.command == 'json-to-csv':
        convert_json_to_csv(args.input_file, args.output_file, args.delimiter, args.escape)

if __name__ == '__main__':
    main()