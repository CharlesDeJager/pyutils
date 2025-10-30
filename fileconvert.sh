#!/bin/bash

# fileconvert.sh - Helper script for file converter utility

# Display help message
show_help() {
    echo "File Converter Utility"
    echo
    echo "Usage:"
    echo "  ./fileconvert.sh csv2json <input.csv> <output.json> [options]"
    echo "  ./fileconvert.sh json2csv <input.json> <output.csv> [options]"
    echo
    echo "Options:"
    echo "  -d, --delimiter <char>   Specify custom delimiter (default: ',')"
    echo "  -e, --escape <char>      Specify escape character"
    echo "  -h, --help              Show this help message"
    echo
    echo "Examples:"
    echo "  ./fileconvert.sh csv2json data.csv output.json"
    echo "  ./fileconvert.sh csv2json data.csv output.json -d ';'"
    echo "  ./fileconvert.sh json2csv data.json output.csv --delimiter '|'"
    echo
}

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Parse arguments
if [ $# -lt 1 ]; then
    show_help
    exit 1
fi

case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    csv2json|json2csv)
        if [ $# -lt 3 ]; then
            echo "Error: Input and output files are required"
            echo "Run './fileconvert.sh --help' for usage information"
            exit 1
        fi
        
        command="$1"
        input_file="$2"
        output_file="$3"
        shift 3

        # Check if input file exists
        if [ ! -f "$input_file" ]; then
            echo "Error: Input file '$input_file' not found"
            exit 1
        fi

        # Convert command name to file-converter format
        case "$command" in
            csv2json) cmd="csv-to-json" ;;
            json2csv) cmd="json-to-csv" ;;
        esac

        # Build and execute the command
        python -m file_converter "$cmd" "$input_file" "$output_file" "$@"
        
        if [ $? -eq 0 ]; then
            echo "Conversion successful: '$input_file' → '$output_file'"
        fi
        ;;
    *)
        echo "Error: Unknown command '$1'"
        echo "Run './fileconvert.sh --help' for usage information"
        exit 1
        ;;
esac