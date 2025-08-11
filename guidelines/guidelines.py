# a library of guidelines classes and their functions for checking them

import inspect
import json
import yaml
from bids import BIDSLayout
from pathlib import Path

class cobidas:
    def __init__(self, layout: BIDSLayout):
        # load in the BIDS layout
        self.layout = layout

        # Load the guidelines from a YAML file
        guidelines_content = yaml.safe_load(
            (Path(__file__).parent / 'cobidas.yaml').read_text(encoding='utf-8')
        )
        self.guidelines = guidelines_content['guidelines']

    def _grade_success(self, tally, total):
        """
        Determine the success status based on the tally and total counts.
        Returns 'not applicable', 'complete failure', 'partial success', or 'complete success'.
        """

        if tally == 0 and total == 0:
            return 'not applicable'
        elif tally == 0 and total != 0:
            return 'complete failure'
        elif tally == total:
            return 'complete success'
        else:
            return 'partial success'

    def _measure_success(self, tally, total):
        """
        Calculate the success percentage based on the tally and total counts.
        Returns the percentage as an integer.
        """

        if total == 0:
            return '0 %'
        else:
            return str( int(round( ( tally / total ) * 100, 0 ) )) + ' %'

    def D01_05_02_00_00_01(self):
        """
        Specify the instructions given to subjects for each condition
        (ideally the exact text in supplement or appendix).
        For resting-state, be sure to indicate eyes-closed, eyes-open, any fixation.
        Describe if the subjects received any rewards during the task,
        and state if there was a familiarization / training inside or outside the scanner
        """

        index = inspect.currentframe().f_code.co_name.replace('_', '.')
        guideline = self.guidelines[index]
        tally = 0
        total = 0

        # logic for this guideline
        for task in self.layout.get_tasks():
            task_files = self.layout.get(task=task, return_type='filename', extension='nii.gz')

            for task_file in task_files:
                total += 1
                metadata = self.layout.get_metadata(task_file)
                if 'Instructions' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'percent_success': self._measure_success(tally, total),
        }

    def D02_02_01_00_00_01(self):
        """
        Provide [MRI] make, model & field strength in tesla (T)
        """

        index = inspect.currentframe().f_code.co_name.replace('_', '.')
        guideline = self.guidelines[index]
        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            total += 1
            metadata = self.layout.get_metadata(nifti_file)
            if 'Manufacturer' in metadata and \
               'ManufacturersModelName' in metadata and \
               'MagneticFieldStrength' in metadata:
                tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'percent_success': self._measure_success(tally, total),
        }

