#! /usr/bin/env python3

# For checking BIDS directories against established guidelines, like COBIDAS.

import argparse
import inspect
import tomllib
import yaml

from bids import BIDSLayout
from guidelines.guidelines import cobidas
from pathlib import Path

def percent_string(value):
    """
    Convert a float value between 0.0 and 1.0 to a percentage string.
    """
    if not (0.0 <= value <= 1.0):
        raise ValueError("Value to cast to percent_string must be between 0.0 and 1.0")

    return str(int(round( value * 100 ))) + ' %'

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
    # for bids_dir in sorted(Path("/data/openneuro/20250530_openneuro_clone").glob("ds004869/")):
    for bids_dir in sorted(Path("/data/openneuro/20250530_openneuro_clone").glob("ds*/")):
    # for bids_dir in Path("C:\\Users\\earlea\\OneDrive - National Institutes of Health\\Desktop\\repo\\bids-examples").glob("*/"):

        if bids_dir.name.startswith('.') or bids_dir.name.startswith('docs') or bids_dir.name.startswith('tools'):
            continue

        if not bids_dir.exists():
            raise FileNotFoundError(f"Error: The specified BIDS directory '{bids_dir}' does not exist.")

        if not bids_dir.is_dir():
            raise ValueError(f"Error: The specified path '{bids_dir}' is not a directory.")

        print(f"Using {args.guidelines} guidelines to check BIDS dataset: {bids_dir}")
        try:
            layout = BIDSLayout(bids_dir, derivatives=False)
        except Exception as e:
            print(f"Error initializing BIDSLayout. Skipping '{bids_dir}':\n{e}")
            continue

        if args.guidelines == 'COBIDAS':
            # Initialize the cobidas class with the BIDS layout
            checker = cobidas(layout)
            guidelines_content = yaml.safe_load(
                (Path(__file__).parent / 'guidelines/cobidas.yaml').read_text(encoding='utf-8')
            )

        elif args.guidelines == 'CLAIM':
            raise ValueError("CLAIM guidelines are not yet implemented.")
            
        elif args.guidelines == 'CRED-nf':
            raise ValueError("CRED-nf guidelines are not yet implemented.")

        # Here you would implement the logic to check the BIDS directory
        guideline_functions = inspect.getmembers(checker, predicate=inspect.ismethod)
        guidelines_score = 0.0
        guidelines_evaluated = 0.0

        # Iterate through the guideline functions and execute them
        for name, func in guideline_functions:
            if name.startswith('_'):
                continue

            index = func.__name__.replace('_', '.')

            try:
                result = func()
                if result['status'] == 'not applicable':
                    continue
                else:
                    guidelines_score += result['success_rate']
                    guidelines_evaluated += 1.0

                    print(f"{index}:\t{result['tally']}/{result['total']}\t({percent_string(result['success_rate'])})\t{guidelines_content['guidelines'][index]['info']}")

            except Exception as e:
                print(f"Error running check {name}: {e}")

        # all done!
        score = percent_string( guidelines_score / guidelines_evaluated ) if guidelines_evaluated > 0 else "Not Applicable"
        print(f"Checked {bids_dir.name} dataset with {int(guidelines_evaluated)} applicable {args.guidelines} guidelines: SCORE = {score}\n")

if __name__ == "__main__":
    main()
