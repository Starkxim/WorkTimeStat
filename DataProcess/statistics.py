import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

def plot_monthly_overtime(file_path):
    # 设置字体为支持中文的字体
    rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    monthly_overtime = calculate_monthly_overtime(file_path)
    plt.figure(figsize=(10, 6))
    monthly_overtime.plot(kind='bar')
    plt.xticks(rotation=0)
    plt.title('每月加班时长')
    plt.xlabel('月份')
    plt.ylabel('加班时长')
    plt.show()

def calculate_monthly_overtime(file_path):
    df = pd.read_excel(file_path)
    df['开始时间'] = pd.to_datetime(df['开始时间'])
    df['月份'] = df['开始时间'].dt.to_period('M')
    
    # 处理时长列，转换为小时数
    df['时长'] = df['时长'].str.replace('小时', '').astype(float)
    
    # 计算每月的计薪和调休加班时长
    monthly_overtime = df.groupby('月份')['时长'].sum()
    
    # 将 PeriodIndex 转换为字符串格式
    monthly_overtime.index = monthly_overtime.index.astype(str)
    
    return monthly_overtime