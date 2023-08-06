#! /usr/bin/env python

import os
from distutils import dir_util
import pytest
from pyrcbm import sin_rcbm

@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir

class TestSinRcbm:
    def check_output_file(self, tmpdir, expected_output_file, test):
        if expected_output_file:
            print('getting output -- CWD: {}'.format(os.getcwd()))
            expected_file = open(expected_output_file, 'r')
            expected_file_content = expected_file.read()
            expected_file.close()
        else:
            expected_file_content = ''

        os.chdir(tmpdir)
        print('tmpdir -- CWD: {}'.format(os.getcwd()))
        sin_rcbm.gen_script(test['offset'], test['amplitude'], test['omega'], test['phi'], test['sample_average'])
        with open('sin_wave.js', 'r') as output_file:
            output_file_content = output_file.read()
            assert output_file_content == expected_file_content

    def test_default(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_default.js'), test)

    def test_offset_in_range_1(self, datadir):
        test = {
            'offset': '1000',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_offset_in_range_1.js'), test)

    def test_offset_in_range_2(self, datadir):
        test = {
            'offset': '2000',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_offset_in_range_2.js'), test)

    def test_offset_out_of_range_1(self, datadir):
        test = {
            'offset': '999',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        with pytest.raises(AssertionError):
            self.check_output_file(datadir, '', test)

    def test_offset_out_of_range_2(self, datadir):
        test = {
            'offset': '2001',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        with pytest.raises(AssertionError):
            self.check_output_file(datadir, '', test)

    def test_amplitude_in_range(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '0',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_amplitude_in_range.js'), test)

    def test_offset_out_of_range_1(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '-1',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        with pytest.raises(AssertionError):
            self.check_output_file(datadir, '', test)

    def test_offset_out_of_range_2(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '501',
            'omega': '1',
            'phi': '0',
            'sample_average': '20',
        }
        with pytest.raises(AssertionError):
            self.check_output_file(datadir, '', test)

    def test_frequency_1(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '0.1',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_frequency_1.js'), test)

    def test_frequency_2(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '99',
            'phi': '0',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_frequency_2.js'), test)

    def test_phase_1(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '1',
            'phi': '6.28',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_phase_1.js'), test)

    def test_phase_2(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '1',
            'phi': '-5',
            'sample_average': '20',
        }
        self.check_output_file(datadir, datadir.join('sin_phase_2.js'), test)

    def test_avg_1(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '1',
        }
        self.check_output_file(datadir, datadir.join('sin_avg_1.js'), test)

    def test_avg_2(self, datadir):
        test = {
            'offset': '1500',
            'amplitude': '500',
            'omega': '1',
            'phi': '0',
            'sample_average': '100',
        }
        self.check_output_file(datadir, datadir.join('sin_avg_2.js'), test)
