from tkinter import Tk, Menu, ttk
import os
import pandas as pd
from ui.utils.Utils_Functions import Update_holidays, select_money_file, select_rest_file, merge_files

# 检测节假日文件是否存在，不存在则更新
def check_holiday_files():
    year = pd.Timestamp.now().year
    holiday_file = os.path.join("HolidayData", f"public_holidays_{year}.csv")
    makeup_workdays_file = os.path.join("HolidayData", f"makeup_workdays_{year}.csv")
    if not os.path.exists(holiday_file) or not os.path.exists(makeup_workdays_file):
        Update_holidays()

def create_main_window():
    global tree
    root = Tk()
    root.focus_force()
    root.title("工作时间处理工具")
    root.geometry("1000x400")

    check_holiday_files()

    menu = Menu(root)
    root.config(menu=menu)

    # 创建“附加”菜单
    additional_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="附加", menu=additional_menu)
    additional_menu.add_command(label="更新节假日和补班日期", command=Update_holidays)

    # 创建“文件”菜单
    file_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="选择计薪加班文件", command=lambda: select_money_file(tree))
    file_menu.add_command(label="选择调休加班文件", command=lambda: select_rest_file(tree))
    file_menu.add_separator()
    file_menu.add_command(label="合并文件", command=lambda: merge_files(tree))

    # 创建Treeview和滚动条
    frame = ttk.Frame(root)
    frame.pack(expand=True, fill='both')

    tree = ttk.Treeview(frame, columns=10, height=10, show='headings')

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')

    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')

    tree.pack(fill="both", expand=True)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    root.mainloop()

if __name__ == "__main__":
    print("程序应该从main.py启动")