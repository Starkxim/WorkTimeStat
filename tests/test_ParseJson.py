import datetime
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
from DataProcess.ParseJson import get_holidays


class TestParseJson(unittest.TestCase):

    @patch("DataProcess.ParseJson.requests.get")
    @patch("DataProcess.ParseJson.pd.DataFrame.to_csv")
    def test_get_holidays_success(self, mock_to_csv, mock_get):
        # Mock the current year
        current_year = datetime.datetime.now().year.__str__()

        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Years": {
                current_year: [
                    {
                        "StartDate": "2023-01-01",
                        "EndDate": "2023-01-03",
                        "CompDays": ["2023-01-06"],
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        get_holidays()

        # Check if the to_csv method was called twice (for public holidays and makeup workdays)
        self.assertEqual(mock_to_csv.call_count, 2)

        # Check the arguments passed to to_csv
        args, kwargs = mock_to_csv.call_args_list[0]
        self.assertTrue(f"HolidayData/public_holidays_{current_year}.csv" in args)
        args, kwargs = mock_to_csv.call_args_list[1]
        self.assertTrue(f"HolidayData/makeup_workdays_{current_year}.csv" in args)

    @patch("DataProcess.ParseJson.requests.get")
    def test_get_holidays_request_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        with self.assertRaises(Exception) as context:
            get_holidays()
        self.assertEqual(
            str(context.exception), "获取节假日和补班日期失败，请检查网络连接"
        )


if __name__ == "__main__":
    unittest.main()
