from tkinter import Tk, filedialog, messagebox, Button, Label
import subprocess
import threading
from DataProcess.excel import merge_files as merge_excel_files
import DataProcess.ParseJson as ParseJson

def Update_holidays():
    ParseJson.get_holidays()

    messagebox.showinfo("完成", "节假日和补班日期已更新并保存在HolidayData文件夹中")

def select_money_file():
    global money_file
    money_file = filedialog.askopenfilename(title="选择计薪加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if money_file:
        messagebox.showinfo("文件选择", f"已选择计薪加班文件: {money_file}")
    else:
        messagebox.showwarning("警告", "未选择计薪加班文件")

def select_rest_file():
    global rest_file
    rest_file = filedialog.askopenfilename(title="选择调休加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if rest_file:
        messagebox.showinfo("文件选择", f"已选择调休加班文件: {rest_file}")
    else:
        messagebox.showwarning("警告", "未选择调休加班文件")

def merge_files():
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

def create_main_window():
    root = Tk()
    root.title("加班文件合并工具")
    root.geometry("300x300")

    Label(root, text="请选择文件并进行合并").pack(pady=10)

    Button(root, text="更新节假日和补班日期", command=Update_holidays).pack(pady=5)
    Button(root, text="选择计薪加班文件", command=select_money_file).pack(pady=5)
    Button(root, text="选择调休加班文件", command=select_rest_file).pack(pady=5)
    Button(root, text="合并文件", command=merge_files).pack(pady=20)

    root.mainloop()