import tkinter as tk
from ui.utils.Utils_Functions import center_window
import os
import pandas as pd
import DataProcess.ParseJson as ParseJson


def check_holiday_files():
    """
    检测节假日文件是否存在，不存在则更新。

    检查当前年份的节假日和补班日期文件是否存在，如果不存在则调用更新函数。
    """
    year = pd.Timestamp.now().year
    holiday_file = os.path.join("HolidayData", f"public_holidays_{year}.csv")
    makeup_workdays_file = os.path.join("HolidayData", f"makeup_workdays_{year}.csv")
    if not os.path.exists(holiday_file) or not os.path.exists(makeup_workdays_file):
        ParseJson.get_holidays()


def show_loading_screen():
    """
    显示加载窗口。

    创建一个Tkinter窗口，显示加载信息，并在3秒后自动关闭。

    """
    loading_root = tk.Tk()
    loading_root.title("正在启动")
    center_window(loading_root, 300, 100)
    label = tk.Label(loading_root, text="正在启动，请稍候...", font=("", 20))
    label.pack(pady=20)
    loading_root.after(3000, loading_root.destroy)  # 显示3秒后关闭加载窗口
    loading_root.mainloop()
