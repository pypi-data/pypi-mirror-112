#! /usr/bin/env python

import os
from distutils import dir_util
import pytest
from pyrcbm import ulog2rcbm

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
        ulog2rcbm.convert_ulog2rcbm(test['filename'], test['multi'], test['actuator'], test['average'])

        output_file_prefix = test['filename']
        if output_file_prefix.lower().endswith('.ulg'):
            output_file_prefix = output_file_prefix[:-4]

        with open('{0}_{1}_{2}_{3}.js'.format(output_file_prefix, 'actuator_outputs', test['multi'], test['actuator']), 'r') as output_file:
            output_file_content = output_file.read()
            assert output_file_content == expected_file_content

    def test_default(self, datadir):
        test = {
            'filename': 'sample1.ulg',
            'multi': '0',
            'actuator': '0',
            'average': '20',
        }
        self.check_output_file(datadir, datadir.join('ulog_default.js'), test)

    def test_actuator_1(self, datadir):
        test = {
            'filename': 'sample1.ulg',
            'multi': '0',
            'actuator': '3',
            'average': '20',
        }
        self.check_output_file(datadir, datadir.join('ulog_actuator_1.js'), test)

    def test_actuator_2(self, datadir):
        test = {
            'filename': 'sample1.ulg',
            'multi': '0',
            'actuator': '15',
            'average': '20',
        }
        self.check_output_file(datadir, datadir.join('ulog_actuator_2.js'), test)

    def test_avg_1(self, datadir):
        test = {
            'filename': 'sample1.ulg',
            'multi': '0',
            'actuator': '0',
            'average': '1',
        }
        self.check_output_file(datadir, datadir.join('ulog_avg_1.js'), test)

    def test_avg_2(self, datadir):
        test = {
            'filename': 'sample1.ulg',
            'multi': '0',
            'actuator': '0',
            'average': '100',
        }
        self.check_output_file(datadir, datadir.join('ulog_avg_2.js'), test)
