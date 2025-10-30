# fileconvert.ps1 - Helper script for file converter utility

# Display help message
function Show-Help {
    Write-Host "File Converter Utility"
    Write-Host
    Write-Host "Usage:"
    Write-Host "  .\fileconvert.ps1 csv2json <input.csv> <output.json> [options]"
    Write-Host "  .\fileconvert.ps1 json2csv <input.json> <output.csv> [options]"
    Write-Host
    Write-Host "Options:"
    Write-Host "  -Delimiter <char>    Specify custom delimiter (default: ',')"
    Write-Host "  -Escape <char>       Specify escape character"
    Write-Host "  -Help               Show this help message"
    Write-Host
    Write-Host "Examples:"
    Write-Host "  .\fileconvert.ps1 csv2json data.csv output.json"
    Write-Host "  .\fileconvert.ps1 csv2json data.csv output.json -Delimiter ';'"
    Write-Host "  .\fileconvert.ps1 json2csv data.json output.csv -Delimiter '|'"
    Write-Host
}

# Check if Python is available
try {
    $null = Get-Command python -ErrorAction Stop
}
catch {
    Write-Error "Error: Python is not installed or not in PATH"
    exit 1
}

# Parse arguments
if ($args.Count -lt 1) {
    Show-Help
    exit 1
}

switch ($args[0]) {
    { $_ -in "-h", "--help", "-Help" } {
        Show-Help
        exit 0
    }
    { $_ -in "csv2json", "json2csv" } {
        if ($args.Count -lt 3) {
            Write-Error "Error: Input and output files are required"
            Write-Host "Run '.\fileconvert.ps1 -Help' for usage information"
            exit 1
        }
        
        $command = $args[0]
        $inputFile = $args[1]
        $outputFile = $args[2]
        
        # Check if input file exists
        if (-not (Test-Path $inputFile)) {
            Write-Error "Error: Input file '$inputFile' not found"
            exit 1
        }
        
        # Convert command name to file-converter format
        $cmd = switch ($command) {
            "csv2json" { "csv-to-json" }
            "json2csv" { "json-to-csv" }
        }
        
        # Get additional arguments
        $extraArgs = @()
        if ($args.Count -gt 3) {
            for ($i = 3; $i -lt $args.Count; $i++) {
                $arg = $args[$i]
                # Convert PowerShell style parameters to Python style
                switch ($arg) {
                    "-Delimiter" { 
                        $extraArgs += "--delimiter"
                        $extraArgs += $args[++$i]
                    }
                    "-Escape" {
                        $extraArgs += "--escape"
                        $extraArgs += $args[++$i]
                    }
                    default {
                        $extraArgs += $arg
                    }
                }
            }
        }
        
        # Build and execute the command
        $pythonArgs = @(
            "-m",
            "file_converter",
            $cmd,
            $inputFile,
            $outputFile
        ) + $extraArgs
        
        & python $pythonArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Conversion successful: '$inputFile' → '$outputFile'"
        }
    }
    default {
        Write-Error "Error: Unknown command '$($args[0])'"
        Write-Host "Run '.\fileconvert.ps1 -Help' for usage information"
        exit 1
    }
}