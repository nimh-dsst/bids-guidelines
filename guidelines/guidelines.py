# a library of guidelines classes and their functions for checking them

import yaml
from bids import BIDSLayout
from copy import deepcopy
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
        Returns "level" of success.
        """

        if tally == 0 and total == 0:
            return 'not applicable'
        elif tally == 0 and total != 0:
            return 'failure'
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
            return 0.0
        else:
            return float(tally) / float(total)

    # D01.05.02.00.00.01
    def D01_05_02_00_00_01(self):
        """
        Table D.1. Experimental Design Reporting | Task specification | Instructions
        ---------------------------------------------
        Specify the instructions given to subjects for each condition
        (ideally the exact text in supplement or appendix).
        For resting-state, be sure to indicate eyes-closed, eyes-open, any fixation.
        Describe if the subjects received any rewards during the task,
        and state if there was a familiarization / training inside or outside the scanner
        """

        tally = 0
        total = 0

        # logic for this guideline
        for task in self.layout.get_tasks():
            task_files = self.layout.get(task=task, extension='nii.gz')

            for task_file in task_files:
                metadata = task_file.get_metadata()

                total += 1
                if 'Instructions' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.02.01.00.00.01
    def D02_02_01_00_00_01(self):
        """
        Table D.2. Acquisition Reporting | MRI system description | Scanner
        ---------------------------------------------
        Provide make, model & field strength in tesla (T)
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['datatype'] in ['anat', 'dwi', 'fmap', 'func', 'perf']:
                total += 1
                if 'Manufacturer' in metadata:
                    tally += 1

                total += 1
                if 'ManufacturersModelName' in metadata:
                    tally += 1

                total += 1
                if 'MagneticFieldStrength' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.02.04.00.00.01
    def D02_02_04_00_00_01(self):
        """
        Table D.2. Acquisition Reporting | MRI system description | Software version
        ---------------------------------------------
        Highly recommended when sharing vendor-specific protocols or exam cards,
        as version may be needed to correctly interpret that information
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['datatype'] in ['anat', 'dwi', 'fmap', 'func', 'perf']:
                total += 1
                if 'SoftwareVersions' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.03.01.00.01
    def D02_03_03_01_00_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Essential sequence & imaging parameters | All acquisitions
        ---------------------------------------------
        Echo time (TE)
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['datatype'] in ['anat', 'dwi', 'fmap', 'func', 'perf']:
                total += 1
                if 'EchoTime' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.03.01.00.02
    def D02_03_03_01_00_02(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Essential sequence & imaging parameters | All acquisitions
        ---------------------------------------------
        Repetition time (TR)
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['datatype'] in ['anat', 'dwi', 'fmap', 'func', 'perf']:
                total += 1
                if 'RepetitionTime' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.03.01.00.03
    def D02_03_03_01_00_03(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Essential sequence & imaging parameters | All acquisitions
        ---------------------------------------------
        Flip angle (FA)
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['datatype'] in ['anat', 'dwi', 'fmap', 'func', 'perf']:
                total += 1
                if 'FlipAngle' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.03.04.00.01
    def D02_03_03_04_00_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Essential sequence & imaging parameters | B0 field maps
        ---------------------------------------------
        Echo time difference (dTE)
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='fmap', extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            if entities['suffix'] in ['magnitude1', 'magnitude2', 'phasediff', 'phase1', 'phase2']:
                total += 1
                if 'EchoTime' in metadata or 'EchoTime1' in metadata or 'EchoTime2' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.03.05.00.03
    def D02_03_03_05_00_03(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Essential sequence & imaging parameters | Diffusion MRI
        ---------------------------------------------
        B-values
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(datatype='dwi', extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            entities = nifti_file.get_entities()

            bval_entities = deepcopy(entities)
            bval_entities['extension'] = '.bval'
            bval = Path(self.layout.build_path(bval_entities))

            bvec_entities = deepcopy(entities)
            bvec_entities['extension'] = '.bvec'
            bvec = Path(self.layout.build_path(bval_entities))

            total += 1
            if bval.exists() and bvec.exists():
                tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.01.01
    def D02_03_18_01_01_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | All acquisitions
        ---------------------------------------------
        Labelling method, e.g. continuous ASL (CASL), pseudo-continuous ASL (PCASL), Pulsed ALS (PASL), velocity selective ASL (VSASL)
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            total += 1
            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] in ["CASL", "PCASL", "PASL"]:
                tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.01.02
    def D02_03_18_01_01_02(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | All acquisitions
        ---------------------------------------------
        Use of background suppression pulses and their timing
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            total += 1
            if 'BackgroundSuppression' in metadata:
                tally += 1

                if metadata['BackgroundSuppression']:
                    total += 1
                    if 'BackgroundSuppressionNumberPulses' in metadata:
                        tally += 1

                    total += 1
                    if 'BackgroundSuppressionPulseTime' in metadata:
                        tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.02.01
    def D02_03_18_01_02_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PCASL or CASL
        ---------------------------------------------
        Label Duration
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] in ["CASL", "PCASL"]:
                total += 1
                if 'LabelingDuration' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.02.02
    def D02_03_18_01_02_02(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PCASL or CASL
        ---------------------------------------------
        Post-labeling delay (PLD)
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] in ["CASL", "PCASL"]:
                total += 1
                if 'PostLabelingDelay' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }
    
    # D02.03.18.01.03.01
    def D02_03_18_01_03_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PCASL
        ---------------------------------------------
        Average labelling gradient
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] == "PCASL":
                total += 1
                if 'LabelingPulseAverageGradient' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.03.03
    def D02_03_18_01_03_03(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PCASL
        ---------------------------------------------
        Flip angle of B1 pulses
        """

        tally = 0
        total = 0

        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] == "PCASL":
                total += 1
                if 'LabelingPulseFlipAngle' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.04.01
    def D02_03_18_01_04_01(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | CASL
        ---------------------------------------------
        Use of a separate labelling coil
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()
            
            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] == "CASL":
                total += 1
                if 'CASLType' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.05.02
    def D02_03_18_01_05_02(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PASL
        ---------------------------------------------
        Labelling slab thickness
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] == "PASL":
                total += 1
                if 'LabelingSlabThickness' in metadata:
                    tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # D02.03.18.01.05.03
    def D02_03_18_01_05_03(self):
        """
        Table D.2. Acquisition Reporting | MRI acquisition | Perfusion | Arterial Spin Labelling MRI | PASL
        ---------------------------------------------
        Use of QUIPSS pulses and their timing
        """

        tally = 0
        total = 0
        
        # logic for this guideline
        for nifti_file in self.layout.get(datatype='perf', extension='nii.gz'):
            metadata = nifti_file.get_metadata()

            if 'ArterialSpinLabelingType' in metadata and metadata['ArterialSpinLabelingType'] == "PASL":
                if 'BolusCutOffFlag' in metadata and metadata['BolusCutOffFlag']:

                    total += 1
                    if 'BolusCutOffTechnique' in metadata:
                        tally += 1

                    total += 1
                    if 'BolusCutOffDelayTime' in metadata:
                        tally += 1

        return {
            'tally': tally,
            'total': total,
            'status': self._grade_success(tally, total),
            'success_rate': self._measure_success(tally, total),
        }

    # 