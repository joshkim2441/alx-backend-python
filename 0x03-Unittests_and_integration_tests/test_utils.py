#!/usr/bin/env python3
"""Test utils.py
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, result):
        """Test access_nested_map
        """
        res = access_nested_map(nested_map, path)
        self.assertEqual(res, result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_output):
        """Test access_nested_map
        """
        with self.assertRaises(expected_output) as context:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json
    """
    @parameterized.expand([
        ("https://example.com", {"payload": True}),
        ("https://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, result):
        """Test get_json
        """
        mock_response = Mock()
        mock_response.json.return_value = result
        with patch('requests.get', return_value=mock_response):
            res = get_json(url)
        self.assertEqual(res, result)


class TestMemoize(unittest.TestCase):
    """Test memoize
    """
    def test_memoize(self):
        """Test memoize
        """
        class TestClass:
            def a_method(self):
                """a_method called"""
                return 42

            @memoize
            def a_property(self):
                """a_property called"""
                return self.a_method()

        test = TestClass()

        with patch.object(test, 'a_method') as mock:
            mock.return_value = 42

            res1 = test.a_property
            res2 = test.a_property

            self.assertEqual(res1, 42)
            self.assertEqual(res1, res2)
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main
