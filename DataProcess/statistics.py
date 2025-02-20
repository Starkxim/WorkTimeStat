import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams


def plot_monthly_overtime(file_path: str):
    """
    绘制每月加班时长柱状图。

    读取指定文件路径的Excel文件，计算每月的加班时长，并绘制柱状图显示。

    Args:
        file_path (str): Excel文件路径。
    """
    # 设置字体为支持中文的字体
    rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体
    rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

    monthly_overtime = calculate_monthly_overtime(file_path)
    plt.figure(figsize=(10, 6))
    monthly_overtime.plot(kind="bar")
    plt.xticks(rotation=0)
    plt.title("每月加班时长")
    plt.xlabel("月份")
    plt.ylabel("加班时长")
    plt.show()


def calculate_monthly_overtime(file_path: str) -> pd.Series:
    """
    计算每月加班时长。

    读取指定文件路径的Excel文件，计算每月的加班时长，并返回结果。

    Args:
        file_path (str): Excel文件路径。

    Returns:
        pd.Series: 每月加班时长的Series对象，索引为月份，值为加班时长。
    """
    df = pd.read_excel(file_path)
    df["开始时间"] = pd.to_datetime(df["开始时间"])
    df["月份"] = df["开始时间"].dt.to_period("M")

    # 处理时长列，转换为小时数
    df["时长"] = df["时长"].str.replace("小时", "").astype(float)

    # 计算每月的计薪和调休加班时长
    monthly_overtime = df.groupby("月份")["时长"].sum()

    # 将 PeriodIndex 转换为字符串格式
    monthly_overtime.index = monthly_overtime.index.astype(str)
    monthly_overtime.index.name = None  # 移除索引名称

    return monthly_overtime
