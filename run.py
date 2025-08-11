#! /usr/bin/env python3

# For checking BIDS directories against established guidelines, like COBIDAS.

import argparse
import inspect
import tomllib

from bids import BIDSLayout
from guidelines.guidelines import cobidas
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
        help='Path to the BIDS dataset directory to check.',
    )
    parser.add_argument(
        '-g', '--guidelines', metavar='GUIDELINE', type=str, default='COBIDAS',
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
    # bids_dir = args.bids_directory
    for bids_dir in Path("C:\\Users\\earlea\\OneDrive - National Institutes of Health\\Desktop\\repo\\bids-guidelines").glob("ds005752/"):
    # for bids_dir in Path("C:\\Users\\earlea\\OneDrive - National Institutes of Health\\Desktop\\repo\\bids-examples").glob("*/"):

        if bids_dir.name.startswith('.') or bids_dir.name.startswith('docs') or bids_dir.name.startswith('tools'):
            continue

        if not bids_dir.exists():
            raise FileNotFoundError(f"Error: The specified BIDS directory '{bids_dir}' does not exist.")

        if not bids_dir.is_dir():
            raise ValueError(f"Error: The specified path '{bids_dir}' is not a directory.")

        print(f"Using {args.guidelines} guidelines to check BIDS dataset: {bids_dir}")
        layout = BIDSLayout(bids_dir)

        if args.guidelines == 'COBIDAS':
            # Initialize the cobidas class with the BIDS layout
            checker = cobidas(layout)

        elif args.guidelines == 'CLAIM':
            raise ValueError("CLAIM guidelines are not yet implemented.")
            
        elif args.guidelines == 'CRED-nf':
            raise ValueError("CRED-nf guidelines are not yet implemented.")

        # Here you would implement the logic to check the BIDS directory
        guideline_functions = inspect.getmembers(checker, predicate=inspect.ismethod)

        for name, func in guideline_functions:
            if name.startswith('_'):
                continue

            try:
                result = func()
                print(f"Result for check {name}: {result['status']}")
            except Exception as e:
                print(f"Error running check {name}: {e}")

        # all done!
        print(f"Finished using {args.guidelines} guidelines to check BIDS dataset: {bids_dir}\n")

if __name__ == "__main__":
    main()
