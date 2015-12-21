import mock
import unittest
from testrail.api import API
from testrail.helper import TestRailError
import copy
import ast


class TestHTTPMethod(unittest.TestCase):
    def setUp(self):
        self.client = API()

    @mock.patch('testrail.api.requests.get')
    def test_get_ok(self, mock_get):
        mock_response = mock.Mock()
        return_value = {
            "announcement": "..",
            "completed_on": None,
            "id": 1,
            "is_completed": False,
            "name": "Datahub",
            "show_announcement": True,
            "url": "http://<server>/index.php?/projects/overview/1"
        }

        expected_response = copy.deepcopy(return_value)
        mock_response.json.return_value = return_value
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'https://<server>/index.php?/api/v2/get_project/1'
        actual_response = self.client._get('get_project/1')
        mock_get.assert_called_once_with(url, headers={'Content-Type': 'application/json'}, params=None, auth=('user@yourdomain.com', 'your_api_key'))
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_bad_no_params(self, mock_get):
        mock_response = mock.Mock()
        expected_response = {
            'url': 'https://<server>/index.php?/api/v2/get_plan/200',
            'status_code': 400,
            'payload': None,
            'error': 'Invalid or unknown test plan'
        }
        url = 'https://<server>/index.php?/api/v2/get_plan/200'
        mock_response.json.return_value = {'error': 'Invalid or unknown test plan'}
        mock_response.status_code = 400
        mock_response.url = url
        mock_get.return_value = mock_response

        with self.assertRaises(TestRailError) as e:
            self.client._get('get_plan/200')
        mock_get.assert_called_once_with(url, headers={'Content-Type': 'application/json'}, params=None, auth=('user@yourdomain.com', 'your_api_key'))
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, ast.literal_eval(str(e.exception)))


if __name__ == "__main__":
    unittest.main()
