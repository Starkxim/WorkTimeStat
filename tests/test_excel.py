import datetime
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd


class TestMergeFiles(unittest.TestCase):

    @patch('DataProcess.excel.pd.read_csv')
    @patch('DataProcess.excel.pd.read_excel')
    @patch('DataProcess.excel.pd.DataFrame.to_excel')
    @patch('DataProcess.excel.load_workbook')
    @patch('DataProcess.excel.os.path.join')
    def test_merge_files_success(self, mock_path_join, mock_load_workbook, mock_to_excel, mock_read_excel, mock_read_csv):
        # Mock the current year
        current_year = datetime.datetime.now().year.__str__()

        # Mock the file paths
        mock_path_join.return_value = 'test_output_file.xlsx'

        # Mock the read_csv function to return test data
        mock_read_csv.side_effect = [
            pd.DataFrame({'date': ['2023-01-01', '2023-01-02', '2023-01-03']}),
            pd.DataFrame({'date': ['2023-01-06']})
        ]

        # Mock the read_excel function to return test data
        mock_read_excel.side_effect = [
            pd.DataFrame({
                '申请人': ['Alice', 'Bob'],
                '开始时间': ['2023-01-01 08:00', '2023-01-02 09:00'],
                '结束时间': ['2023-01-01 12:00', '2023-01-02 13:00'],
                '时长': [4, 4],
                '项目编号': ['P001', 'P002'],
                '当前审批状态': ['已通过', '已通过']
            }),
            pd.DataFrame({
                '申请人': ['Alice', 'Bob'],
                '开始时间': ['2023-01-01 08:00', '2023-01-02 09:00'],
                '结束时间': ['2023-01-01 12:00', '2023-01-02 13:00'],
                '加班时长': [4, 4],
                '项目编号': ['P001', 'P002'],
                '当前审批状态': ['已通过', '已通过']
            })
        ]

        # Mock the load_workbook function
        mock_wb = MagicMock()