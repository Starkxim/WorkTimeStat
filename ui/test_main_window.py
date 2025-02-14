import unittest
from unittest.mock import patch

from DataProcess.excel import merge_files
from ui.main_window import Update_holidays, select_money_file, select_rest_file


class TestMainWindow(unittest.TestCase):

    @patch('ui.main_window.ParseJson.get_holidays')
    @patch('ui.main_window.messagebox.showinfo')
    def test_Update_holidays(self, mock_showinfo, mock_get_holidays):
        Update_holidays()
        mock_get_holidays.assert_called_once()
        mock_showinfo.assert_called_once_with("完成", "节假日和补班日期已更新并保存在HolidayData文件夹中")

    @patch('ui.main_window.filedialog.askopenfilename')
    @patch('ui.main_window.messagebox.showinfo')
    @patch('ui.main_window.messagebox.showwarning')
    def test_select_money_file(self, mock_showwarning, mock_showinfo, mock_askopenfilename):
        # Test when a file is selected
        mock_askopenfilename.return_value = 'test_money_file.xlsx'
        select_money_file()
        mock_showinfo.assert_called_once_with("文件选择", "已选择计薪加班文件: test_money_file.xlsx")
        mock_showwarning.assert_not_called()

        # Test when no file is selected
        mock_askopenfilename.return_value = ''
        select_money_file()
        mock_showwarning.assert_called_once_with("警告", "未选择计薪加班文件")

    @patch('ui.main_window.filedialog.askopenfilename')
    @patch('ui.main_window.messagebox.showinfo')
    @patch('ui.main_window.messagebox.showwarning')
    def test_select_rest_file(self, mock_showwarning, mock_showinfo, mock_askopenfilename):
        # Test when a file is selected
        mock_askopenfilename.return_value = 'test_rest_file.xlsx'
        select_rest_file()
        mock_showinfo.assert_called_once_with("文件选择", "已选择调休加班文件: test_rest_file.xlsx")
        mock_showwarning.assert_not_called()

        # Test when no file is selected
        mock_askopenfilename.return_value = ''
        select_rest_file()
        mock_showwarning.assert_called_once_with("警告", "未选择调休加班文件")

    @patch('ui.main_window.filedialog.askdirectory')
    @patch('ui.main_window.filedialog.askopenfilename')
    @patch('ui.main_window.messagebox.showwarning')
    @patch('ui.main_window.messagebox.showinfo')
    @patch('ui.main_window.messagebox.showerror')
    @patch('ui.main_window.merge_excel_files')
    @patch('ui.main_window.subprocess.Popen')
    def test_merge_files(self, mock_Popen, mock_merge_excel_files, mock_showerror, mock_showinfo, mock_showwarning, mock_askopenfilename, mock_askdirectory):
        global money_file, rest_file

        # Test when no files are selected
        money_file = ''
        rest_file = ''
        save_directory = ''
        merge_files(money_file, rest_file, save_directory)
        mock_showwarning.assert_called_once_with("警告", "请先选择两个Excel文件")

        # Test when files are selected but no directory is chosen
        money_file = 'test_money_file.xlsx'
        rest_file = 'test_rest_file.xlsx'
        save_directory = ''
        mock_askdirectory.return_value = ''
        merge_files(money_file, rest_file, save_directory)
        mock_showwarning.assert_called_with("警告", "未选择保存文件的文件夹")

        # Test successful merge
        save_directory = 'test_directory'
        mock_askdirectory.return_value = 'test_directory'
        mock_merge_excel_files.return_value = 'output_file.xlsx'
        merge_files(money_file, rest_file, save_directory)
        mock_merge_excel_files.assert_called_once_with('test_money_file.xlsx', 'test_rest_file.xlsx', 'test_directory')
        mock_showinfo.assert_called_once_with("完成", f"数据合并和排序完成！结果已保存到: output_file.xlsx")