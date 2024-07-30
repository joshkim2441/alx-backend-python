#!/usr/bin/env python3
"""Familiarize yourself with the utils.access_nested_map function and
understand its purpose. Play with it in the Python console to make
sure you understand.

In this task you will write the first unit test for utils.access_nested_map.

Create a TestAccessNestedMap class that inherits from unittest.TestCase.

Implement the TestAccessNestedMap.test_access_nested_map method to test that
the method returns what it is supposed to.

Decorate the method with @parameterized.expand to test the function for
ollowing inputs:

nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
"""

import unittest
from typing import Dict
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, result):
        """Test access_nested_map"""
        res = access_nested_map(nested_map, path)
        self.assertEqual(res, result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         result):
        """Test access_nested_map"""
        with self.assertRaises(result) as context:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json"""

    @parameterized.expand([
        ("https://example.com", {"payload": True}),
        ("https://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict,
    ) -> None:
        """Test get_json"""
        attrs = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**attrs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test memoize"""
    def test_memoize(self):
        """Test memoize"""

        class TestClass:
            """TestClass"""

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
            self.assertEqual(res1, 42)
            mock.assert_called_once()
