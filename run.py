#! /usr/bin/env python3

# For checking BIDS directories against established guidelines, like COBIDAS.

import argparse
import tomllib
from pathlib import Path

def cli():
    # read version from the pyproject.toml file
    version_file = Path(__file__).parent / 'pyproject.toml'
    with open(version_file, 'rb') as f:
        version_data = tomllib.load(f)

    version = version_data['project']['version']

    # create the argument parser
    parser = argparse.ArgumentParser(description='BIDS Guidelines App CLI')

    parser.add_argument(
        'bids_directory', metavar='BIDS_DIR', type=Path,
        help='Path to the BIDS directory to check.',
    )
    parser.add_argument(
        '-g', '--guidelines', type=str, default='COBIDAS',
        choices=['COBIDAS', 'CLAIM', 'CRED-nf'],
        help='Guidelines to check against. Default is COBIDAS.',
    )
    parser.add_argument(
        '-v', '--version', action='version', version=version,
        help='Show the version of the BIDS Guidelines App CLI and quit.',
    )

    return parser.parse_args()

def main():
    args = cli()


if __name__ == "__main__":
    main()
