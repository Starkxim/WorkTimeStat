from tkinter import filedialog, messagebox
import threading
import subprocess
import pandas as pd
from DataProcess.excel import merge_files as merge_excel_files
import DataProcess.ParseJson as ParseJson
from DataProcess.statistics import calculate_monthly_overtime, plot_monthly_overtime

def search_tree(tree, search_text):
    global data
    for item in tree.get_children():
        tree.delete(item)

    for row in data:
        if search_text.lower() in str(row).lower():
            tree.insert('', 'end', values=row)

def show_monthly_overtime(tree):
    global combined_file_path
    combined_file_path = filedialog.askopenfilename(title="选择合并的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not combined_file_path:
        messagebox.showwarning("警告", "请先合并文件")
        return
    monthly_overtime = calculate_monthly_overtime(combined_file_path)
    messagebox.showinfo("每月加班时长", str(monthly_overtime))

def show_overtime_chart(tree):
    global combined_file_path
    combined_file_path = filedialog.askopenfilename(title="选择合并的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not combined_file_path:
        messagebox.showwarning("警告", "请先合并文件")
        return
    plot_monthly_overtime(combined_file_path)

def Update_holidays():
    def run_update():
        ParseJson.get_holidays()
        messagebox.showinfo("更新完成！", "节假日和补班日期已更新，保存于HolidayData文件夹")

    threading.Thread(target=run_update).start()

def display_excel(tree, file_path):
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
    global money_file
    money_file = filedialog.askopenfilename(title="选择计薪加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if money_file:
        messagebox.showinfo("文件选择", f"已选择计薪加班文件: {money_file}")
        display_excel(tree, money_file)
    else:
        messagebox.showwarning("警告", "未选择计薪加班文件")

def select_rest_file(tree):
    global rest_file
    rest_file = filedialog.askopenfilename(title="选择调休加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if rest_file:
        messagebox.showinfo("文件选择", f"已选择调休加班文件: {rest_file}")
        display_excel(tree, rest_file)
    else:
        messagebox.showwarning("警告", "未选择调休加班文件")

def merge_files(tree):
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
        subprocess.Popen(['start', output_file], shell=True)

    threading.Thread(target=run_merge).start()