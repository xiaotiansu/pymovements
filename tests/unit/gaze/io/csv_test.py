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
"""Test read from csv."""
import polars as pl
import pytest

import pymovements as pm


@pytest.mark.parametrize(
    ('kwargs', 'shape'),
    [
        pytest.param(
            {
                'file': 'tests/files/monocular_example.csv',
                'time_column': 'time',
                'time_unit': 'ms',
                'pixel_columns': ['x_left_pix', 'y_left_pix'],
            },
            (10, 2),
            id='csv_mono_shape',
        ),
        pytest.param(
            {
                'file': 'tests/files/binocular_example.csv',
                'time_column': 'time',
                'time_unit': 'ms',
                'pixel_columns': ['x_left_pix', 'y_left_pix', 'x_right_pix', 'y_right_pix'],
                'position_columns': ['x_left_pos', 'y_left_pos', 'x_right_pos', 'y_right_pos'],
            },
            (10, 3),
            id='csv_bino_shape',
        ),
        pytest.param(
            {
                'file': 'tests/files/hbn_example.csv',
                'time_column': pm.Dataset('HBN', path='').definition.time_column,
                'time_unit': pm.Dataset('HBN', path='').definition.time_unit,
                'experiment': pm.Dataset('HBN', path='').definition.experiment,
                'pixel_columns': pm.Dataset('HBN', path='').definition.pixel_columns,
            },
            (10, 2),
            id='hbn_dataset_example',
        ),
        pytest.param(
            {
                'file': 'tests/files/sbsat_example.csv',
                'time_column': pm.Dataset('SBSAT', '').definition.time_column,
                'time_unit': pm.Dataset('SBSAT', '').definition.time_unit,
                'pixel_columns': pm.Dataset('SBSAT', '').definition.pixel_columns,
                **pm.Dataset('SBSAT', '').definition.custom_read_kwargs['gaze'],
            },
            (10, 5),
            id='sbsat_dataset_example',
        ),
        pytest.param(
            {
                'file': 'tests/files/gazebase_example.csv',
                'time_column': pm.Dataset('GazeBase', '').definition.time_column,
                'time_unit': pm.Dataset('GazeBase', '').definition.time_unit,
                'position_columns': pm.Dataset('GazeBase', '').definition.position_columns,
                **pm.Dataset('GazeBase', '').definition.custom_read_kwargs['gaze'],
            },
            (10, 7),
            id='gazebase_dataset_example',
        ),
        pytest.param(
            {
                'file': 'tests/files/gaze_on_faces_example.csv',
                'time_column': pm.Dataset('GazeOnFaces', '').definition.time_column,
                'time_unit': pm.Dataset('GazeOnFaces', '').definition.time_unit,
                'pixel_columns': pm.Dataset('GazeOnFaces', '').definition.pixel_columns,
                **pm.Dataset('GazeOnFaces', '').definition.custom_read_kwargs['gaze'],
            },
            (10, 1),
            id='gaze_on_faces_dataset_example',
        ),
        pytest.param(
            {
                'file': 'tests/files/gazebase_vr_example.csv',
                'time_column': pm.Dataset('GazeBaseVR', '').definition.time_column,
                'time_unit': pm.Dataset('GazeBaseVR', '').definition.time_unit,
                'position_columns': pm.Dataset('GazeBaseVR', '').definition.position_columns,
            },
            (10, 11),
            id='gazebase_vr_dataset_example',
        ),
        pytest.param(
            {
                'file': 'tests/files/judo1000_example.csv',
                'time_column': pm.Dataset('JuDo1000', '').definition.time_column,
                'time_unit': pm.Dataset('JuDo1000', '').definition.time_unit,
                'pixel_columns': pm.Dataset('JuDo1000', '').definition.pixel_columns,
                **pm.Dataset('JuDo1000', '').definition.custom_read_kwargs['gaze'],
            },
            (10, 4),
            id='judo1000_dataset_example',
        ),
    ],
)
def test_shapes(kwargs, shape):
    gaze_dataframe = pm.gaze.from_csv(**kwargs)
    assert gaze_dataframe.frame.shape == shape


@pytest.mark.parametrize(
    ('kwargs', 'schema_overrides'),
    [
        pytest.param(
            {
                'file': 'tests/files/monocular_example.csv',
                'time_column': 'time',
                'time_unit': 'ms',
                'pixel_columns': ['x_left_pix', 'y_left_pix'],
            },
            [pl.Int64, pl.List(pl.Int64)],
            id='csv_mono_schema_overrides',
        ),
        pytest.param(
            {
                'file': 'tests/files/missing_values_example.csv',
                'time_column': 'time',
                'time_unit': 'ms',
                'pixel_columns': ['pixel_x', 'pixel_y'],
                'position_columns': ['position_x', 'position_y'],
            },
            [pl.Int64, pl.List(pl.Float64), pl.List(pl.Float64)],
            id='csv_missing_values_schema_overrides',
        ),
    ],
)
def test_schema_overrides(kwargs, schema_overrides):
    gaze_dataframe = pm.gaze.from_csv(**kwargs)
    assert gaze_dataframe.frame.dtypes == schema_overrides
