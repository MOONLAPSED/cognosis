"""
This module contains tests for the `application` module in the cognosis project.
It includes tests that verify the functionality of the application components, ensuring they perform as expected.
"""
import unittest
from unittest.mock import patch

import pytest
from cognosis.application import broker
from cognosis.FSK_mono.mono import UUID
from faststream.kafka import TestKafkaBroker
from main import Entity_, main, run_tests


class EntityPublisherTestCasePublisher(unittest.TestCase):
    @patch("main.Entity_.publish")
    def test_publisher(self, mock_publish):
        entity = main.Entity_()
        topic = "test_topic"
        message = "test_message"

        mock_publish.return_value = None

        # Call the publisher method
        publisher = entity.publisher(topic)
        result = publisher(message)

        # Assert that the publish method was called with the correct arguments
        mock_publish.assert_called_once_with(topic, message)

        # Assert that the result is None
        self.assertIsNone(result)

    @patch("cognosis.main.Entity_.publish")
    def test_publisher(self, mock_publish):
        entity = Entity_()
        topic = "test_topic"
        message = "test_message"

        mock_publish.return_value = None

        # Call the publisher method
        publisher = entity.publisher(topic)
        result = publisher(message)

        # Assert that the publish method was called with the correct arguments
        mock_publish.assert_called_once_with(topic, message)

        # Assert that the result is None
        self.assertIsNone(result)
        entity = Entity_()
        topic = "test_topic"
        message = "test_message"

        mock_publish.return_value = None

        # Call the publisher method
        publisher = entity.publisher(topic)
        result = publisher(message)

        # Assert that the publish method was called with the correct arguments
        mock_publish.assert_called_once_with(topic, message)

        # Assert that the result is None
        self.assertIsNone(result)


class TestRunTestsRunTests(unittest.TestCase):
    @patch("unittest.main")
    def test_run_tests(self, mock_main):
        run_tests()
        mock_main.assert_called_once()

    @patch("unittest.main")
    def test_run_tests(self, mock_main):
        run_tests()
        mock_main.assert_called_once()

    @patch("unittest.main")
    @patch("logging.error")
    def test_run_tests_exception_handling(self, mock_error, mock_main):
        mock_main.side_effect = Exception("Test exception")
        run_tests()
        mock_main.assert_called_once()
        mock_error.assert_called_once_with("Error running tests: Test exception")


class EntityTestPublish(unittest.TestCase):
    @patch("builtins.print")
    def test_publish(self, mock_print):
        entity = Entity_()
        entity.publish("topic", "message")
        mock_print.assert_called_once_with("Publishing message: message")

    @patch("builtins.print")
    def test_publish(self, mock_print):
        entity = Entity_()
        entity.publish("topic", "message")
        mock_print.assert_called_once_with("Publishing message: message")

    @patch("builtins.print")
    def test_publish_with_integer_topic_and_message(self, mock_print):
        entity = Entity_()
        entity.publish(123, 456)
        mock_print.assert_called_once_with("Publishing message: 456")

    @patch("builtins.print")
    def test_publish_with_float_topic_and_message(self, mock_print):
        entity = Entity_()
        entity.publish(3.14, 2.718)
        mock_print.assert_called_once_with("Publishing message: 2.718")

    @patch("builtins.print")
    def test_publish_with_list_topic_and_message(self, mock_print):
        entity = Entity_()
        entity.publish([1, 2, 3], [4, 5, 6])
        mock_print.assert_called_once_with("Publishing message: [4, 5, 6]")

    @patch("builtins.print")
    def test_publish_with_dict_topic_and_message(self, mock_print):
        entity = Entity_()
        entity.publish({"key": "value"}, {"key": "new value"})
        mock_print.assert_called_once_with("Publishing message: {'key': 'new value'}")

    @patch("builtins.print")
    def test_publish_with_none_topic_and_message(self, mock_print):
        entity = Entity_()
        entity.publish(None, None)
        mock_print.assert_called_once_with("Publishing message: None")

    @patch("builtins.print")
    def test_publish_with_non_string_topic(self, mock_print):
        entity = Entity_()
        with self.assertRaises(TypeError):
            entity.publish(123, "message")

    @patch("builtins.print")
    def test_publish_with_non_string_message(self, mock_print):
        entity = Entity_()
        with self.assertRaises(TypeError):
            entity.publish("topic", 456)


class TestMainMain(unittest.TestCase):
    def test_main(self):
        # No need to mock any entities or use the patch decorator
        # Simply call the main method and assert that it runs without any exceptions
        main()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("unittest.TestLoader().discover")
    @patch("unittest.TextTestRunner().run")
    @patch("socketserver.TCPServer")
    def test_main(self, mock_parse_args, mock_discover, mock_run, mock_TCPServer):
        # Mock the return value of argparse.ArgumentParser.parse_args
        mock_args = mock_parse_args.return_value
        mock_args.prompt = ["Test prompt"]

        # Mock the return value of unittest.TestLoader().discover
        mock_suite = mock_discover.return_value

        # Mock the return value of unittest.TextTestRunner().run
        mock_result = mock_run.return_value
        mock_result.wasSuccessful.return_value = True

        # Call the main method
        main()

        # Assert that the mocks were called as expected
        mock_parse_args.assert_called_once()
        mock_discover.assert_called_once_with(start_dir=".", pattern="test_*.py")
        mock_run.assert_called_once_with(mock_suite)
        mock_TCPServer.assert_not_called()


if __name__ == "__main__":
    unittest.main()
