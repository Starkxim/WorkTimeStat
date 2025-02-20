from tkinter import filedialog, messagebox
import threading
import subprocess
import pandas as pd
from DataProcess.excel import merge_files as merge_excel_files
import DataProcess.ParseJson as ParseJson
from DataProcess.statistics import calculate_monthly_overtime, plot_monthly_overtime


def center_window(root, width: int, height: int):
    """
    居中窗口。

    根据屏幕尺寸和指定的宽度、高度，将窗口居中显示。

    Args:
        root (Tk): Tkinter窗口对象。
        width (int): 窗口宽度。
        height (int): 窗口高度。
    """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = "%dx%d+%d+%d" % (
        width,
        height,
        (screenwidth - width) / 2,
        (screenheight - height) / 2,
    )
    root.geometry(size)
    root.update()


def search_tree(tree, search_text: str):
    """
    搜索Treeview中的内容。

    根据搜索文本在Treeview中搜索匹配的行，并显示结果。

    Args:
        tree (Treeview): Tkinter Treeview对象。
        search_text (str): 搜索文本。
    """
    global data
    if "data" not in globals():
        messagebox.showwarning("警告", "没有数据可供搜索")
        return

    for item in tree.get_children():
        tree.delete(item)

    for row in data:
        if search_text.lower() in str(row).lower():
            tree.insert("", "end", values=row)


def show_monthly_overtime(tree):
    """
    显示每月加班时长。

    选择合并的Excel文件，计算每月加班时长，并显示结果。

    Args:
        tree (Treeview): Tkinter Treeview对象。
    """
    global combined_file_path
    combined_file_path = filedialog.askopenfilename(
        title="选择合并的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not combined_file_path:
        messagebox.showwarning("警告", "请先合并文件")
        return
    monthly_overtime = calculate_monthly_overtime(combined_file_path)
    messagebox.showinfo("每月加班时长", str(monthly_overtime))


def show_overtime_chart(tree):
    """
    显示加班时长图表。

    选择合并的Excel文件，绘制每月加班时长的柱状图。

    Args:
        tree (Treeview): Tkinter Treeview对象。
    """
    global combined_file_path
    combined_file_path = filedialog.askopenfilename(
        title="选择合并的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not combined_file_path:
        messagebox.showwarning("警告", "请先合并文件")
        return
    plot_monthly_overtime(combined_file_path)


def Update_holidays():
    """
    更新节假日和补班日期。

    调用ParseJson模块的函数获取最新的节假日和补班日期，并显示更新完成的消息。
    """

    def run_update():
        ParseJson.get_holidays()
        messagebox.showinfo(
            "更新完成！", "节假日和补班日期已更新，保存于HolidayData文件夹"
        )

    threading.Thread(target=run_update).start()


def display_excel(tree, file_path: str):
    """
    显示Excel文件内容。

    读取指定路径的Excel文件，并在Treeview中显示其内容。

    Args:
        tree (Treeview): Tkinter Treeview对象。
        file_path (str): Excel文件路径。
    """
    global data
    df = pd.read_excel(file_path)
    data = df.values.tolist()  # 将 DataFrame 转换为列表并存储到全局变量 data 中
    tree["column"] = list(df.columns)
    tree["show"] = "headings"
    for col in tree["column"]:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))


def select_money_file(tree):
    """
    选择计薪加班文件。

    打开文件选择对话框，选择计薪加班的Excel文件，并在Treeview中显示其内容。

    Args:
        tree (Treeview): Tkinter Treeview对象。
    """
    global money_file
    money_file = filedialog.askopenfilename(
        title="选择计薪加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if money_file:
        messagebox.showinfo("文件选择", f"已选择计薪加班文件: {money_file}")
        display_excel(tree, money_file)
    else:
        messagebox.showwarning("警告", "未选择计薪加班文件")


def select_rest_file(tree):
    """
    选择调休加班文件。

    打开文件选择对话框，选择调休加班的Excel文件，并在Treeview中显示其内容。

    Args:
        tree (Treeview): Tkinter Treeview对象。
    """
    global rest_file
    rest_file = filedialog.askopenfilename(
        title="选择调休加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if rest_file:
        messagebox.showinfo("文件选择", f"已选择调休加班文件: {rest_file}")
        display_excel(tree, rest_file)
    else:
        messagebox.showwarning("警告", "未选择调休加班文件")


def merge_files(tree):
    """
    合并计薪和调休加班文件。

    选择保存结果文件的文件夹，合并计薪和调休加班的Excel文件，并保存结果。

    Args:
        tree (Treeview): Tkinter Treeview对象。
    """
    if not money_file or not rest_file:
        messagebox.showwarning("警告", "请先选择两个Excel文件")
        return

    save_directory = filedialog.askdirectory(title="选择保存结果文件的文件夹")
    if not save_directory:
        messagebox.showwarning("警告", "未选择保存文件的文件夹")
        return

    def run_merge():
        try:
            output_file = merge_excel_files(money_file, rest_file, save_directory)
        except Exception as e:
            messagebox.showerror("错误", str(e))
            return

        messagebox.showinfo("完成", f"数据合并和排序完成！结果已保存到: {output_file}")
        subprocess.Popen(["start", output_file], shell=True)

    threading.Thread(target=run_merge).start()
