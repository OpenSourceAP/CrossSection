"""Run from repo root with the project environment:
PATH=/opt/venv/projects/openap/bin:$PATH python3 -m unittest discover -s Signals/tests -p test_download_failures.py

Inputs: synthetic ZIP/JSON responses and mocked HTTP calls in child processes.
Outputs: unittest results and temporary Parquet files, removed after each test.
No network requests, credentials, WRDS connections, or project data are used.
"""

from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import pandas as pd


DOWNLOADS = Path(__file__).resolve().parents[1] / 'pyCode/DataDownloads'
PIN_CSV = (
    'permno,year,a,eb,es,u,d\n'
    '12345,1981,0.25,5.5,15.2,0.12,0.65\n'
    '23456,1982,0.23,5.8,14.8,0.14,0.62\n'
)

# Run the real entry point so a swallowed error or successful placeholder exit
# fails the test. Every request is intercepted before the script is executed.
OFFLINE_RUNNER = '''
import json
from pathlib import Path
import runpy
import sys
from unittest.mock import Mock, patch

import requests

script, scenario_path = sys.argv[1:]
scenario = json.loads(Path(scenario_path).read_text())
sys.path.insert(0, str(Path(script).parent.parent))
import config
config.DEBUG_MODE = False

response = Mock()
response.headers = {'content-type': 'application/zip'}
response.json.return_value = scenario.get('json', {})
if scenario.get('archive'):
    response.iter_content.return_value = [Path(scenario['archive']).read_bytes()]
request = Mock(return_value=response)
kind = scenario.get('kind')
if kind == 'timeout':
    request.side_effect = requests.exceptions.Timeout('mock source timed out')
elif kind == 'connection_error':
    request.side_effect = requests.exceptions.ConnectionError('mock source unavailable')
elif kind == 'http_error':
    response.raise_for_status.side_effect = requests.exceptions.HTTPError('503 source unavailable')

with patch('dotenv.load_dotenv'), patch('requests.get', request):
    try:
        runpy.run_path(script, run_name='__main__')
    finally:
        expected_calls = 0 if kind == 'missing_key' else 1
        assert request.call_count == expected_calls, 'Unexpected request count or retry'
'''


class DownloadFailureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.working_dir = self.root / 'pyCode'
        self.working_dir.mkdir()
        self.output_dir = self.root / 'pyData/Intermediate'
        self.output_dir.mkdir(parents=True)

    def archive(self, contents):
        data = BytesIO()
        with zipfile.ZipFile(data, 'w', compression=zipfile.ZIP_STORED) as archive:
            for name, value in contents.items():
                archive.writestr(name, value)
            # Meet the production download's minimum-size check with a valid ZIP.
            archive.writestr('padding.txt', 'x' * 2048)
        path = self.root / 'response.zip'
        path.write_bytes(data.getvalue())
        return str(path)

    def run_download(self, name, scenario):
        scenario_path = self.root / 'scenario.json'
        scenario_path.write_text(json.dumps(scenario))
        environment = os.environ.copy()
        environment.pop('FRED_API_KEY', None)
        if scenario.get('kind') != 'missing_key':
            environment['FRED_API_KEY'] = 'offline-test-key'
        environment['PYTHONDONTWRITEBYTECODE'] = '1'
        return subprocess.run(
            [sys.executable, '-c', OFFLINE_RUNNER, str(DOWNLOADS / name), str(scenario_path)],
            cwd=self.working_dir,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def assert_failed_without_output(self, name, output_name, scenario, message):
        output = self.output_dir / output_name
        for has_previous_output in [False, True]:
            with self.subTest(script=name, scenario=scenario.get('kind'), existing=has_previous_output):
                previous_bytes = b'previous successful output'
                if has_previous_output:
                    output.write_bytes(previous_bytes)
                else:
                    output.unlink(missing_ok=True)
                result = self.run_download(name, scenario)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(message, result.stderr)
                self.assertNotIn('Creating placeholder file', result.stdout)
                if has_previous_output:
                    self.assertEqual(output.read_bytes(), previous_bytes)
                else:
                    self.assertFalse(output.exists())

    def test_pin_network_and_http_failures_exit_with_error(self):
        for kind in ['timeout', 'connection_error', 'http_error']:
            self.assert_failed_without_output(
                'PINData.py', 'pin_monthly.parquet', {'kind': kind},
                'PIN source download or parsing failed',
            )

    def test_pin_invalid_archive_and_unreadable_csv_exit_with_error(self):
        broken_archive = self.root / 'broken.zip'
        broken_archive.write_bytes(b'not a zip archive' * 200)
        for archive in [str(broken_archive), self.archive({'pin_yearly.csv': ''})]:
            self.assert_failed_without_output(
                'PINData.py', 'pin_monthly.parquet', {'archive': archive},
                'PIN source download or parsing failed',
            )

    def test_pin_missing_archive_member_does_not_use_leftover_csv(self):
        stale_source = self.output_dir / 'pin_yearly.csv'
        stale_source.write_text(PIN_CSV)
        self.assert_failed_without_output(
            'PINData.py', 'pin_monthly.parquet',
            {'archive': self.archive({'unrelated.csv': PIN_CSV})},
            'pin_yearly.csv',
        )
        self.assertEqual(stale_source.read_text(), PIN_CSV)

    def test_pin_success_preserves_values_and_eleven_month_lag(self):
        result = self.run_download('PINData.py', {'archive': self.archive({'pin_yearly.csv': PIN_CSV})})
        self.assertEqual(result.returncode, 0, result.stderr)
        output = pd.read_parquet(self.output_dir / 'pin_monthly.parquet')
        self.assertEqual(len(output), 24)
        self.assertEqual(output['permno'].tolist(), [12345] * 12 + [23456] * 12)
        self.assertEqual(str(output['permno'].dtype), 'int64')
        self.assertEqual(output['month'].tolist(), list(range(1, 13)) * 2)
        expected_values = {
            'a': (0.25, 0.23), 'eb': (5.5, 5.8), 'es': (15.2, 14.8),
            'u': (0.12, 0.14), 'd': (0.65, 0.62),
        }
        for column, (first, second) in expected_values.items():
            self.assertEqual(output[column].tolist(), [first] * 12 + [second] * 12)
        expected_months = pd.date_range('1981-12-01', periods=24, freq='MS')
        self.assertEqual(output['time_avail_m'].tolist(), expected_months.tolist())

    def test_gnp_missing_key_exits_before_requesting_data(self):
        self.assert_failed_without_output(
            'GNPDeflator.py', 'GNPdefl.parquet', {'kind': 'missing_key'},
            'FRED_API_KEY is required',
        )

    def test_gnp_network_and_http_failures_exit_with_error(self):
        errors = {'timeout': 'mock source timed out', 'connection_error': 'mock source unavailable',
                  'http_error': '503 source unavailable'}
        for kind, message in errors.items():
            self.assert_failed_without_output(
                'GNPDeflator.py', 'GNPdefl.parquet', {'kind': kind}, message,
            )

    def test_gnp_missing_numeric_observations_exit_with_error(self):
        self.assert_failed_without_output(
            'GNPDeflator.py', 'GNPdefl.parquet',
            {'json': {'observations': [{'date': '1981-01-01', 'value': '.'}]}},
            'no usable numeric observations',
        )

    def test_gnp_success_preserves_ratio_and_three_month_lag(self):
        observations = [
            {'date': '1981-01-01', 'value': '123.4'},
            {'date': '1981-04-01', 'value': '125.0'},
            {'date': '1981-07-01', 'value': '.'},
        ]
        result = self.run_download('GNPDeflator.py', {'json': {'observations': observations}})
        self.assertEqual(result.returncode, 0, result.stderr)
        output = pd.read_parquet(self.output_dir / 'GNPdefl.parquet')
        self.assertEqual(output.columns.tolist(), ['time_avail_m', 'gnpdefl'])
        self.assertEqual(output['time_avail_m'].tolist(),
                         pd.date_range('1981-04-01', periods=6, freq='MS').tolist())
        self.assertEqual(output['gnpdefl'].tolist(), [123.4 / 100] * 3 + [1.25] * 3)


if __name__ == '__main__':
    unittest.main()
