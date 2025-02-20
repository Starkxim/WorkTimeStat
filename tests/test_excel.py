import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMergeFiles(unittest.TestCase):
    """
    测试合并文件功能的单元测试类。
    """

    @patch("DataProcess.excel.pd.read_csv")
    @patch("DataProcess.excel.pd.read_excel")
    @patch("DataProcess.excel.pd.DataFrame.to_excel")
    @patch("DataProcess.excel.load_workbook")
    @patch("DataProcess.excel.os.path.join")
    def test_merge_files_success(
        self,
        mock_path_join: MagicMock,
        mock_load_workbook: MagicMock,
        mock_to_excel: MagicMock,
        mock_read_excel: MagicMock,
        mock_read_csv: MagicMock,
    ):
        """
        测试合并文件成功的情况。

        模拟读取CSV和Excel文件，合并数据并保存结果文件。

        Args:
            mock_path_join (MagicMock): 模拟os.path.join函数。
            mock_load_workbook (MagicMock): 模拟load_workbook函数。
            mock_to_excel (MagicMock): 模拟DataFrame.to_excel函数。
            mock_read_excel (MagicMock): 模拟pd.read_excel函数。
            mock_read_csv (MagicMock): 模拟pd.read_csv函数。
        """

        # Mock the file paths
        mock_path_join.return_value = "test_output_file.xlsx"

        # Mock the read_csv function to return test data
        mock_read_csv.side_effect = [
            pd.DataFrame({"date": ["2023-01-01", "2023-01-02", "2023-01-03"]}),
            pd.DataFrame({"date": ["2023-01-06"]}),
        ]

        # Mock the read_excel function to return test data
        mock_read_excel.side_effect = [
            pd.DataFrame(
                {
                    "申请人": ["Alice", "Bob"],
                    "开始时间": ["2023-01-01 08:00", "2023-01-02 09:00"],
                    "结束时间": ["2023-01-01 12:00", "2023-01-02 13:00"],
                    "时长": [4, 4],
                    "项目编号": ["P001", "P002"],
                    "当前审批状态": ["已通过", "已通过"],
                }
            ),
            pd.DataFrame(
                {
                    "申请人": ["Alice", "Bob"],
                    "开始时间": ["2023-01-01 08:00", "2023-01-02 09:00"],
                    "结束时间": ["2023-01-01 12:00", "2023-01-02 13:00"],
                    "加班时长": [4, 4],
                    "项目编号": ["P001", "P002"],
                    "当前审批状态": ["已通过", "已通过"],
                }
            ),
        ]


if __name__ == "__main__":
    unittest.main()
