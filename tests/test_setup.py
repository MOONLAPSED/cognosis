import unittest
from unittest.mock import patch

from app.setup import RateLimitExceededError, run_setup


class TestSetup(unittest.TestCase):
    @patch('subprocess.run')
    def test_run_setup_rate_limit_exceeded(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=['./setup.sh'],
            returncode=0,
            stdout='',
            stderr='Error: Setup job has been run too many times. Please wait and try again.'
        )

        with self.assertRaises(RateLimitExceededError):
            run_setup()

    @patch('subprocess.run')
    def test_run_setup_success(self, mock_run):
        expected_output = 'Setup job completed successfully'
        mock_run.return_value = subprocess.CompletedProcess(
            args=['./setup.sh'],
            returncode=0,
            stdout=expected_output,
            stderr=''
        )

        result = run_setup()
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
