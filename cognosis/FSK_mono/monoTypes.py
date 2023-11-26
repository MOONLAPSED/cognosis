import unittest
from time import time
from unittest import TestCase, mock
from unittest.mock import patch

from cognosis.FSK_mono.monoTypes import Entity_, Kerneltuple_


class KerneltupleTestCase(TestCase):
    @mock.patch("time.sleep")
    def test_get_values(self, mock_sleep):
        # Set up the mock return value
        mock_sleep.return_value = None

        # Create an instance of Kerneltuple_
        kerneltuple = Kerneltuple_()

        # Call the get_values method
        values = kerneltuple.get_values()

        # Assert the expected behavior
        self.assertEqual(values, kerneltuple.values)

    @patch("time.sleep")
    def test_get_values_with_different_values(self, mock_sleep):
        # Set up the mock return value
        mock_sleep.return_value = None

        # Create an instance of Kerneltuple_
        values = [1, 2, 3]
        kerneltuple = Kerneltuple_(values=values)

        # Call the get_values method
        result = kerneltuple.get_values()

        # Assert the expected behavior
        self.assertEqual(result, values)

    @patch("time.sleep")
    def test_get_values_with_empty_values(self, mock_sleep):
        # Set up the mock return value
        mock_sleep.return_value = None

        # Create an instance of Kerneltuple_
        values = []
        kerneltuple = Kerneltuple_(values=values)

        # Call the get_values method
        result = kerneltuple.get_values()

        # Assert the expected behavior
        self.assertEqual(result, values)

    @patch("time.sleep")
    def test_get_values_with_retry(self, mock_sleep):
        # Set up the mock return value
        mock_sleep.return_value = None

        # Create an instance of Kerneltuple_
        values = [1, 2, 3]
        kerneltuple = Kerneltuple_(values=values)

        # Set up the mock return value for the retry loop
        mock_kerneltuple = mock.Mock(side_effect=[Exception(), kerneltuple])
        with patch("cognosis.FSK_mono.monoTypes.Kerneltuple_", mock_kerneltuple):
            # Call the get_values method
            result = kerneltuple.get_values()

        # Assert the expected behavior
        self.assertEqual(result, values)
        self.assertEqual(mock_kerneltuple.call_count, 2)
        mock_sleep.assert_called_with(2)


class EntityTestCaseRepr(unittest.TestCase):
    @patch("cognosis.FSK_mono.monoTypes.Entity_.name", "mock name")
    @patch("cognosis.FSK_mono.monoTypes.Entity_.description", "mock description")
    def test_entity_repr(self):
        entity = Entity_()
        repr_str = entity.__repr__()
        self.assertEqual(
            repr_str, "Entity_(name='mock name', description='mock description')"
        )

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name", "mock name")
    @patch("cognosis.FSK_mono.monoTypes.Entity_.description", "mock description")
    def test_entity_repr(self):
        entity = Entity_()
        repr_str = entity.__repr__()
        self.assertEqual(
            repr_str, "Entity_(name='mock name', description='mock description')"
        )

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name", "another mock name")
    @patch(
        "cognosis.FSK_mono.monoTypes.Entity_.description", "another mock description"
    )
    def test_entity_repr_different_values(self):
        entity = Entity_()
        repr_str = entity.__repr__()
        self.assertEqual(
            repr_str,
            "Entity_(name='another mock name', description='another mock description')",
        )

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name", "")
    @patch("cognosis.FSK_mono.monoTypes.Entity_.description", "")
    def test_entity_repr_empty_values(self):
        entity = Entity_()
        repr_str = entity.__repr__()
        self.assertEqual(repr_str, "Entity_(name='', description='')")


class TestEntityStr(unittest.TestCase):
    @patch("cognosis.FSK_mono.monoTypes.Entity_.name")
    def test_entity_str(self, mock_name):
        mock_name.return_value = "mocked name"
        entity = Entity_()
        self.assertEqual(str(entity), "mocked name")

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name")
    def test_entity_str(self, mock_name):
        mock_name.return_value = "mocked name"
        entity = Entity_()
        self.assertEqual(str(entity), "mocked name")

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name")
    def test_entity_str_empty_name(self, mock_name):
        mock_name.return_value = ""
        entity = Entity_()
        self.assertEqual(str(entity), "")

    @patch("cognosis.FSK_mono.monoTypes.Entity_.name")
    def test_entity_str_long_name(self, mock_name):
        mock_name.return_value = "a" * 1000
        entity = Entity_()
        self.assertEqual(str(entity), "a" * 1000)


class TestEntity___str__Str(unittest.TestCase):
    @patch("cognosis.FSK_mono.monoTypes.Attribute_.name")
    def test_Entity___str__(self, mock_name):
        mock_name.return_value = "mocked name"

        attribute = Attribute_("test_attribute", "Test attribute")
        result = attribute.__str__()

        self.assertEqual(result, "mocked name")

    @patch("cognosis.FSK_mono.monoTypes.Attribute_.name")
    def test_Attribute___str__(self, mock_name):
        mock_name.return_value = "mocked name"

        attribute = Attribute_("test_attribute", "Test attribute")
        result = attribute.__str__()

        self.assertEqual(result, "mocked name")

    @patch("cognosis.FSK_mono.monoTypes.Attribute_.name")
    def test_Attribute___str__EmptyName(self, mock_name):
        mock_name.return_value = ""

        attribute = Attribute_("test_attribute", "Test attribute")
        result = attribute.__str__()

        self.assertEqual(result, "")

    @patch("cognosis.FSK_mono.monoTypes.Attribute_.name")
    def test_Attribute___str__WhitespaceName(self, mock_name):
        mock_name.return_value = "   "

        attribute = Attribute_("test_attribute", "Test attribute")
        result = attribute.__str__()

        self.assertEqual(result, "   ")


if __name__ == "__main__":
    unittest.main()

