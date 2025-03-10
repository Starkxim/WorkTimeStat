import datetime
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import requests

# 确保可以导入 DataProcess 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from DataProcess.ParseJson import get_holidays


class TestParseJson(unittest.TestCase):
    """
    测试ParseJson模块的单元测试类。
    """

    @patch("DataProcess.ParseJson.requests.get")
    @patch("DataProcess.ParseJson.pd.DataFrame.to_csv")
    def test_get_holidays_success(self, mock_to_csv: MagicMock, mock_get: MagicMock):
        """
        测试成功获取节假日和补班日期的情况。

        模拟requests.get函数返回成功的响应，并检查是否正确调用了to_csv方法保存数据。

        Args:
            mock_to_csv (MagicMock): 模拟pd.DataFrame.to_csv函数。
            mock_get (MagicMock): 模拟requests.get函数。
        """
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
    @patch("DataProcess.ParseJson.messagebox.showerror")
    def test_get_holidays_request_failure(
        self, mock_showerror: MagicMock, mock_get: MagicMock
    ):
        """
        测试获取节假日和补班日期请求失败的情况。

        模拟requests.get函数抛出请求异常，并检查是否正确抛出了自定义异常。

        Args:
            mock_get (MagicMock): 模拟requests.get函数。
            mock_showerror (MagicMock): 模拟messagebox.showerror函数。
        """
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        with self.assertRaises(Exception) as context:
            get_holidays()
        self.assertEqual(
            str(context.exception), "获取节假日和补班日期失败，请检查网络连接"
        )
        self.assertEqual(mock_showerror.call_count, 2)
        mock_showerror.assert_any_call(
            "警告！", "请求中国节假日API失败: Request failed。\n尝试使用备用数据源。"
        )
        mock_showerror.assert_any_call(
            "警告！", "备用数据源请求失败: Request failed。\n请检查网络连接并手动获取数据。若仍无数据，可以自行填写节假日及补班数据。"
        )


if __name__ == "__main__":
    unittest.main()
