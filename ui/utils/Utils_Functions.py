from tkinter import filedialog, messagebox
import threading
import subprocess
import pandas as pd
from DataProcess.excel import merge_files as merge_excel_files
import DataProcess.ParseJson as ParseJson

def Update_holidays():
    def run_update():
        ParseJson.get_holidays()
        messagebox.showinfo("更新完成！", "节假日和补班日期已更新，保存于HolidayData文件夹")

    threading.Thread(target=run_update).start()

def display_excel(tree, file_path):
    df = pd.read_excel(file_path)
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