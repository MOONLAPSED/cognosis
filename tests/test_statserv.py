import unittest

from statserv import Statserv


class TestStatserv(unittest.TestCase):
    def test_help(self):
        # Test case 1: Verify that help() returns the expected output
        statserv = Statserv()
        expected_output = "This is the help message"
        self.assertEqual(statserv.help(), expected_output)

        # Test case 2: Verify that help() handles empty input
        statserv = Statserv()
        expected_output = "No help available"
        self.assertEqual(statserv.help(""), expected_output)

        # Test case 3: Verify that help() handles invalid input
        statserv = Statserv()
        expected_output = "Invalid command"
        self.assertEqual(statserv.help("invalid"), expected_output)

        # Test case 4: Verify that help() handles special characters
        statserv = Statserv()
        expected_output = "Special characters not supported"
        self.assertEqual(statserv.help("!@#$"), expected_output)

if __name__ == '__main__':
    unittest.main()
