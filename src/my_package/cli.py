"""
Command-line interface for my_package.
"""
import argparse
import sys
from typing import Optional

from my_package.main import run_application


def main(args: Optional[list[str]] = None) -> None:
    """
    CLI entry point that processes command line arguments.

    Args:
        args: Optional list of command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Example Python CLI utility',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--option',
        help='Custom message to print instead of default greeting'
    )

    parsed_args = parser.parse_args(args)

    try:
        run_application(parsed_args.option)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
