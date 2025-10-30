# fileconvert.ps1 - Helper script for file converter utility

# Find and activate virtual environment
function Find-And-Activate-Venv {
    $projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    $venvDirs = @("venv", ".venv", "env", ".env")
    
    foreach ($venvDir in $venvDirs) {
        $activateScript = Join-Path $projectRoot $venvDir "Scripts" "Activate.ps1"
        
        if (Test-Path $activateScript) {
            & $activateScript
            return $true
        }
    }
    
    Write-Error "Error: No virtual environment found in common locations (venv, .venv, env, .env)"
    Write-Host "Please create and activate a virtual environment first:"
    Write-Host "  python -m venv venv"
    Write-Host "  .\\venv\\Scripts\\Activate.ps1"
    Write-Host "  pip install -e ."
    exit 1
}

# Ensure we're in a virtual environment
if (-not $env:VIRTUAL_ENV) {
    Find-And-Activate-Venv
}

# Process multiple files
function Convert-FilesBulk {
    param(
        [string]$Command,
        [string]$InputPattern,
        [string]$OutputDir,
        [array]$ExtraArgs
    )
    
    # Ensure output directory exists
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    
    $count = 0
    $errors = 0
    
    # Get all matching input files
    Get-ChildItem -Path $InputPattern | ForEach-Object {
        $inputFile = $_.FullName
        
        # Determine output filename
        $outputFile = switch ($Command) {
            "csv2json" { Join-Path $OutputDir "$($_.BaseName).json" }
            "json2csv" { Join-Path $OutputDir "$($_.BaseName).csv" }
        }
        
        # Convert command name to file-converter format
        $cmd = switch ($Command) {
            "csv2json" { "csv-to-json" }
            "json2csv" { "json-to-csv" }
        }
        
        # Convert file
        Write-Host "Converting: $inputFile → $outputFile"
        
        $pythonArgs = @(
            "-m",
            "file_converter",
            $cmd,
            $inputFile,
            $outputFile
        ) + $ExtraArgs
        
        & python $pythonArgs
        
        if ($LASTEXITCODE -eq 0) {
            $count++
        } else {
            $errors++
        }
    }
    
    Write-Host
    Write-Host "Conversion complete:"
    Write-Host "  Successful: $count"
    Write-Host "  Failed: $errors"
    Write-Host "  Output directory: $OutputDir"
}

# Display help message
function Show-Help {
    Write-Host "File Converter Utility"
    Write-Host
    Write-Host "Usage:"
    Write-Host "Single file conversion:"
    Write-Host "  .\fileconvert.ps1 csv2json <input.csv> <output.json> [options]"
    Write-Host "  .\fileconvert.ps1 json2csv <input.json> <output.csv> [options]"
    Write-Host
    Write-Host "Bulk conversion:"
    Write-Host "  .\fileconvert.ps1 csv2json-bulk <input-pattern> <output-dir> [options]"
    Write-Host "  .\fileconvert.ps1 json2csv-bulk <input-pattern> <output-dir> [options]"
    Write-Host
    Write-Host "Options:"
    Write-Host "  -Delimiter <char>    Specify custom delimiter (default: ',')"
    Write-Host "  -Escape <char>       Specify escape character"
    Write-Host "  -Help               Show this help message"
    Write-Host
    Write-Host "Examples:"
    Write-Host "  # Single file conversion"
    Write-Host "  .\fileconvert.ps1 csv2json data.csv output.json"
    Write-Host "  .\fileconvert.ps1 csv2json data.csv output.json -Delimiter ';'"
    Write-Host
    Write-Host "  # Bulk conversion"
    Write-Host "  .\fileconvert.ps1 csv2json-bulk '.\data\*.csv' .\output"
    Write-Host "  .\fileconvert.ps1 json2csv-bulk '.\data\**\*.json' .\output -Delimiter '|'"
    Write-Host
    Write-Host "Note: For bulk conversion, use quotes around file patterns"
    Write-Host "      Supports recursive matching with **"
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
    { $_ -in "csv2json-bulk", "json2csv-bulk" } {
        if ($args.Count -lt 3) {
            Write-Error "Error: Input pattern and output directory are required"
            Write-Host "Run '.\fileconvert.ps1 -Help' for usage information"
            exit 1
        }
        
        $command = $args[0] -replace '-bulk$',''
        $inputPattern = $args[1]
        $outputDir = $args[2]
        
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
        
        Convert-FilesBulk -Command $command -InputPattern $inputPattern -OutputDir $outputDir -ExtraArgs $extraArgs
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