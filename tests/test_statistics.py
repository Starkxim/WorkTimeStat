import unittest
import pandas as pd
from pandas.testing import assert_series_equal
from DataProcess.statistics import calculate_monthly_overtime

class TestStatistics(unittest.TestCase):

    def setUp(self):
        # 创建一个测试用的DataFrame
        data = {
            '申请人': ['丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '丁嫚嫚', '乔超'],
            '开始时间': ['2025/01/18 18:00', '2025/01/19 13:30', '2025/01/20 18:00', '2025/01/02 18:00', '2025/01/04 13:30', '2025/01/06 18:00', '2025/01/14 18:00', '2025/01/15 18:00', '2025/01/02 18:00'],
            '结束时间': ['2025/01/18 21:30', '2025/01/19 20:00', '2025/01/20 21:00', '2025/01/02 21:00', '2025/01/04 17:30', '2025/01/06 21:55', '2025/01/14 21:30', '2025/01/15 23:59', '2025/01/02 21:00'],
            '时长': ['3.5小时', '6.5小时', '3.0小时', '3.0小时', '4.0小时', '3.5小时', '3.5小时', '6.0小时', '3.0小时'],
            '类型': ['计薪', '', '', '调休', '', '', '', '', '计薪'],
            '项目编号': ['101D.20250020：XY_B_D20250020_BSW', '101D.20250020：XY_B_D20250020_BSW', '', '101D.20240042：KOSTAL_JMC_D20240042_BCM', '', '101D.20250020：XY_B_D20250020_BSW', '', '', '101D.20240002：KOSTAL_LP3_D20240002_SBW'],
            '项目计薪总时长': ['13.0小时', '', '', '', '', '19.0小时', '', '', '3.0小时'],
            '项目调休总时长': ['', '', '', '7.0小时', '', '', '', '', ''],
            '调休总时长': ['', '', '', '', '', '', '', '', ''],
            '计薪总时长': ['13.0小时', '', '', '', '', '', '', '', '8.0小时']
        }
        self.df = pd.DataFrame(data)
        self.df['开始时间'] = pd.to_datetime(self.df['开始时间'])

    def test_calculate_monthly_overtime(self):
        # 将测试用的DataFrame保存为Excel文件
        test_file_path = 'test_combined_file.xlsx'
        self.df.to_excel(test_file_path, index=False)

        # 计算每月加班时长
        result = calculate_monthly_overtime(test_file_path)

        # 预期结果
        expected_data = {
            '2025-01': 33.0
        }
        expected = pd.Series(expected_data, name='时长').astype(float)

        # 断言结果是否相等
        assert_series_equal(result, expected)

if __name__ == '__main__':
    unittest.main()