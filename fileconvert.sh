#!/bin/bash

# fileconvert.sh - Helper script for file converter utility

# Find and activate virtual environment
find_and_activate_venv() {
    local venv_dirs=("venv" ".venv" "env" ".env")
    local project_root="$(dirname "$(realpath "$0")")"
    
    for venv_dir in "${venv_dirs[@]}"; do
        local activate_script="$project_root/$venv_dir/bin/activate"
        # Check for Windows Git Bash path
        local win_activate_script="$project_root/$venv_dir/Scripts/activate"
        
        if [ -f "$activate_script" ]; then
            source "$activate_script"
            return 0
        elif [ -f "$win_activate_script" ]; then
            source "$win_activate_script"
            return 0
        fi
    done
    
    echo "Error: No virtual environment found in common locations (venv, .venv, env, .env)"
    echo "Please create and activate a virtual environment first:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate  # Linux/Mac"
    echo "  venv\\Scripts\\activate     # Windows"
    echo "  pip install -e ."
    exit 1
}

# Ensure we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    find_and_activate_venv
fi

# Process multiple files
process_bulk() {
    local command="$1"
    local input_pattern="$2"
    local output_dir="$3"
    local args=("${@:4}")  # All remaining arguments
    local count=0
    local errors=0
    
    # Ensure output directory exists
    mkdir -p "$output_dir"
    
    # Get all matching input files
    for input_file in $input_pattern; do
        if [ ! -f "$input_file" ]; then
            continue
        fi
        
        # Determine output filename
        local basename=$(basename "$input_file")
        local output_file
        case "$command" in
            csv2json)
                output_file="$output_dir/${basename%.*}.json"
                ;;
            json2csv)
                output_file="$output_dir/${basename%.*}.csv"
                ;;
        esac
        
        # Convert file
        echo "Converting: $input_file → $output_file"
        python -m file_converter "$cmd" "$input_file" "$output_file" "${args[@]}"
        
        if [ $? -eq 0 ]; then
            count=$((count + 1))
        else
            errors=$((errors + 1))
        fi
    done
    
    echo
    echo "Conversion complete:"
    echo "  Successful: $count"
    echo "  Failed: $errors"
    echo "  Output directory: $output_dir"
}

# Display help message
show_help() {
    echo "File Converter Utility"
    echo
    echo "Usage:"
    echo "Single file conversion:"
    echo "  ./fileconvert.sh csv2json <input.csv> <output.json> [options]"
    echo "  ./fileconvert.sh json2csv <input.json> <output.csv> [options]"
    echo
    echo "Bulk conversion:"
    echo "  ./fileconvert.sh csv2json-bulk <input-pattern> <output-dir> [options]"
    echo "  ./fileconvert.sh json2csv-bulk <input-pattern> <output-dir> [options]"
    echo
    echo "Options:"
    echo "  -d, --delimiter <char>   Specify custom delimiter (default: ',')"
    echo "  -e, --escape <char>      Specify escape character"
    echo "  -h, --help              Show this help message"
    echo
    echo "Examples:"
    echo "  # Single file conversion"
    echo "  ./fileconvert.sh csv2json data.csv output.json"
    echo "  ./fileconvert.sh csv2json data.csv output.json -d ';'"
    echo
    echo "  # Bulk conversion"
    echo "  ./fileconvert.sh csv2json-bulk './data/*.csv' ./output"
    echo "  ./fileconvert.sh json2csv-bulk './data/**/*.json' ./output -d '|'"
    echo
    echo "Note: For bulk conversion, use quotes around file patterns"
    echo "      Supports globstar (**) for recursive matching if enabled"
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
    csv2json-bulk|json2csv-bulk)
        if [ $# -lt 3 ]; then
            echo "Error: Input pattern and output directory are required"
            echo "Run './fileconvert.sh --help' for usage information"
            exit 1
        fi
        
        command="${1%-bulk}"  # Remove -bulk suffix
        input_pattern="$2"
        output_dir="$3"
        shift 3
        
        # Enable globstar if available (for ** pattern)
        if [ -n "$BASH" ]; then
            shopt -s globstar 2>/dev/null
        fi
        
        # Convert command name to file-converter format
        case "$command" in
            csv2json) cmd="csv-to-json" ;;
            json2csv) cmd="json-to-csv" ;;
        esac
        
        process_bulk "$command" "$input_pattern" "$output_dir" "$@"
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