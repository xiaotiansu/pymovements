# Copyright (c) 2023-2025 The pymovements Project Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Test basic preprocessing on various gaze files."""
import os.path

import pytest

import pymovements as pm


@pytest.fixture(
    name='gaze_from_kwargs',
    params=[
        'csv_monocular',
        'csv_binocular',
        'ipc_monocular',
        'ipc_binocular',
        'eyelink_monocular',
        'eyelink_monocular_2khz',
        'eyelink_monocular_no_dummy',
        'didec',
        'emtec',
        'hbn',
        'sbsat',
        'gaze_on_faces',
        'gazebase',
        'gazebase_vr',
        'judo1000',
        'potec',
    ],
)
def fixture_gaze_init_kwargs(request):
    init_param_dict = {
        'csv_monocular': {
            'file': 'tests/files/monocular_example.csv',
            'time_column': 'time',
            'time_unit': 'ms',
            'pixel_columns': ['x_left_pix', 'y_left_pix'],
            'experiment': pm.Experiment(1024, 768, 38, 30, 60, 'center', 1000),
        },
        'csv_binocular': {
            'file': 'tests/files/binocular_example.csv',
            'time_column': 'time',
            'time_unit': 'ms',
            'pixel_columns': ['x_left_pix', 'y_left_pix', 'x_right_pix', 'y_right_pix'],
            'position_columns': ['x_left_pos', 'y_left_pos', 'x_right_pos', 'y_right_pos'],
            'experiment': pm.Experiment(1024, 768, 38, 30, 60, 'center', 1000),
        },
        'ipc_monocular': {
            'file': 'tests/files/monocular_example.feather',
            'experiment': pm.Experiment(1024, 768, 38, 30, 60, 'center', 1000),
        },
        'ipc_binocular': {
            'file': 'tests/files/binocular_example.feather',
            'experiment': pm.Experiment(1024, 768, 38, 30, 60, 'center', 1000),
        },
        'eyelink_monocular': {
            'file': 'tests/files/eyelink_monocular_example.asc',
            'experiment': pm.DatasetLibrary.get('ToyDatasetEyeLink').experiment,
        },
        'eyelink_monocular_2khz': {
            'file': 'tests/files/eyelink_monocular_2khz_example.asc',
            'experiment': pm.Experiment(
                1280, 1024, 38, 30.2, 68, 'upper left',
                eyetracker=pm.EyeTracker(
                    sampling_rate=2000.0, left=True, right=False,
                    model='EyeLink Portable Duo', vendor='EyeLink',
                ),
            ),
        },
        'eyelink_monocular_no_dummy': {
            'file': 'tests/files/eyelink_monocular_no_dummy_example.asc',
            'experiment': pm.Experiment(
                1920, 1080, 38, 30.2, 68, 'upper left',
                eyetracker=pm.EyeTracker(
                    sampling_rate=500.0, left=True, right=False,
                    model='EyeLink 1000 Plus', vendor='EyeLink',
                ),
            ),
        },
        'didec': {
            'file': 'tests/files/didec_example.txt',
            'time_column': pm.DatasetLibrary.get('DIDEC').time_column,
            'time_unit': pm.DatasetLibrary.get('DIDEC').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('DIDEC').pixel_columns,
            'experiment': pm.DatasetLibrary.get('DIDEC').experiment,
            **pm.DatasetLibrary.get('DIDEC').custom_read_kwargs['gaze'],
        },
        'emtec': {
            'file': 'tests/files/emtec_example.csv',
            'time_column': pm.DatasetLibrary.get('EMTeC').time_column,
            'time_unit': pm.DatasetLibrary.get('EMTeC').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('EMTeC').pixel_columns,
            'experiment': pm.DatasetLibrary.get('EMTeC').experiment,
            **pm.DatasetLibrary.get('EMTeC').custom_read_kwargs['gaze'],
        },
        'hbn': {
            'file': 'tests/files/hbn_example.csv',
            'time_column': pm.DatasetLibrary.get('HBN').time_column,
            'time_unit': pm.DatasetLibrary.get('HBN').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('HBN').pixel_columns,
            'experiment': pm.DatasetLibrary.get('HBN').experiment,
        },
        'sbsat': {
            'file': 'tests/files/sbsat_example.csv',
            'time_column': pm.DatasetLibrary.get('SBSAT').time_column,
            'time_unit': pm.DatasetLibrary.get('SBSAT').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('SBSAT').pixel_columns,
            'experiment': pm.DatasetLibrary.get('SBSAT').experiment,
            'trial_columns': pm.DatasetLibrary.get('SBSAT').trial_columns,
            **pm.DatasetLibrary.get('SBSAT').custom_read_kwargs['gaze'],
        },
        'gaze_on_faces': {
            'file': 'tests/files/gaze_on_faces_example.csv',
            'time_column': pm.DatasetLibrary.get('GazeOnFaces').time_column,
            'time_unit': pm.DatasetLibrary.get('GazeOnFaces').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('GazeOnFaces').pixel_columns,
            'experiment': pm.DatasetLibrary.get('GazeOnFaces').experiment,
            **pm.DatasetLibrary.get('GazeOnFaces').custom_read_kwargs['gaze'],
        },
        'gazebase': {
            'file': 'tests/files/gazebase_example.csv',
            'time_column': pm.DatasetLibrary.get('GazeBase').time_column,
            'time_unit': pm.DatasetLibrary.get('GazeBase').time_unit,
            'position_columns': pm.DatasetLibrary.get('GazeBase').position_columns,
            'experiment': pm.DatasetLibrary.get('GazeBase').experiment,
        },
        'gazebase_vr': {
            'file': 'tests/files/gazebase_vr_example.csv',
            'time_column': pm.DatasetLibrary.get('GazeBaseVR').time_column,
            'time_unit': pm.DatasetLibrary.get('GazeBaseVR').time_unit,
            'position_columns': pm.DatasetLibrary.get('GazeBaseVR').position_columns,
            'experiment': pm.DatasetLibrary.get('GazeBaseVR').experiment,
        },
        'judo1000': {
            'file': 'tests/files/judo1000_example.csv',
            'time_column': pm.DatasetLibrary.get('JuDo1000').time_column,
            'time_unit': pm.DatasetLibrary.get('JuDo1000').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('JuDo1000').pixel_columns,
            'experiment': pm.DatasetLibrary.get('JuDo1000').experiment,
            **pm.DatasetLibrary.get('JuDo1000').custom_read_kwargs['gaze'],
        },
        'potec': {
            'file': 'tests/files/potec_example.tsv',
            'time_column': pm.DatasetLibrary.get('PoTeC').time_column,
            'time_unit': pm.DatasetLibrary.get('PoTeC').time_unit,
            'pixel_columns': pm.DatasetLibrary.get('PoTeC').pixel_columns,
            'experiment': pm.DatasetLibrary.get('PoTeC').experiment,
            **pm.DatasetLibrary.get('PoTeC').custom_read_kwargs['gaze'],
        },

    }
    yield init_param_dict[request.param]


def test_gaze_file_processing(gaze_from_kwargs):
    # Load in gaze file.
    file_extension = os.path.splitext(gaze_from_kwargs['file'])[1]
    gaze = None
    if file_extension in {'.csv', '.tsv', '.txt'}:
        gaze = pm.gaze.from_csv(**gaze_from_kwargs)
    elif file_extension in {'.feather', '.ipc'}:
        gaze = pm.gaze.from_ipc(**gaze_from_kwargs)
    elif file_extension == '.asc':
        gaze = pm.gaze.from_asc(**gaze_from_kwargs)

    assert gaze is not None
    assert gaze.frame.height > 0

    # Do some basic transformations.
    if 'pixel' in gaze.columns:
        gaze.pix2deg()
    gaze.pos2vel()
    gaze.pos2acc()
    gaze.resample(resampling_rate=2000)

    assert 'position' in gaze.columns
    assert 'velocity' in gaze.columns
    assert 'acceleration' in gaze.columns
