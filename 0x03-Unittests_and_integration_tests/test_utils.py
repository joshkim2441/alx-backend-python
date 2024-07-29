#!/usr/bin/env python3
"""Test utils.py
"""
import unittest
from typing import Dict
from requests import HTTPError
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient
from unittest.mock import (
    Mock, MagicMock, PropertyMock, patch,
)
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')

    def test_org(self, org: str, result: dict,
                 mocked_function: MagicMock) -> None:
        """_summary_

        Args:
            org (str): _description_
            result (dict): _description_
            mocked_function (MagicMock): _description_
        """
        mocked_function.return_value = MagicMock(
            return_value=result)
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), result)
        mocked_function.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos(self) -> None:
        """Test public_repos
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   ) as mock_org:
                   mock_org.return_value = {
                       "repos_url": "https://api.github.com/users/google/repos",
                   }
                   self.assertEqual(
                       GithubOrgClient("google")._public_repos_url,
                       "https://api.github.com/users/google/repos"
                   )
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test public_repos

        Args:
            mock_get_json (MagicMock): _description_
        """
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    'id': 8566972,
                    'name': 'kratu',
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }

        mock_get_json.return_value = test_payload["repos"]
        with patch('client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
               GithubOrgClient("google").public_repos(),
               ["episodes.dart", "kratu"],
           )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()


    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Test the 'has_license' method"""
        gh_org_client = GithubOrgClient("google")
        client_has_license = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_license, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """_summary_

    Args:
            unittest (_type_): _description_

    Returns:
            _type_: _description_
    """

    @classmethod
    def setUpClass(cls) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """_summary_
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """_summary_
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(license='apache-2.0'),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """_summary_
        """
        cls.get_patcher.stop()



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
