from tkinter import Tk, filedialog, messagebox, Button, Label, Menu, ttk
import subprocess
import threading
import pandas as pd
from DataProcess.excel import merge_files as merge_excel_files
import DataProcess.ParseJson as ParseJson

def Update_holidays():
    ParseJson.get_holidays()
    messagebox.showinfo("完成", "节假日和补班日期已更新并保存在HolidayData文件夹中")

def display_excel(tree, file_path):
    df = pd.read_excel(file_path)
    tree["column"] = list(df.columns)
    tree["show"] = "headings"
    for col in tree["column"]:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def select_money_file():
    global money_file
    money_file = filedialog.askopenfilename(title="选择计薪加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if money_file:
        messagebox.showinfo("文件选择", f"已选择计薪加班文件: {money_file}")
        display_excel(tree, money_file)
    else:
        messagebox.showwarning("警告", "未选择计薪加班文件")

def select_rest_file():
    global rest_file
    rest_file = filedialog.askopenfilename(title="选择调休加班的Excel文件", filetypes=[("Excel files", "*.xlsx *.xls")])
    if rest_file:
        messagebox.showinfo("文件选择", f"已选择调休加班文件: {rest_file}")
        display_excel(tree, rest_file)
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
    global tree
    root = Tk()
    root.title("加班文件合并工具")
    root.geometry("600x400")

    menu = Menu(root)
    root.config(menu=menu)

    fm = Menu(menu, tearoff=False)
    menu.add_cascade(label="附加", menu=fm)
    fm.add_command(label="更新节假日和补班日期", command=Update_holidays)

    Label(root, text="请选择文件并进行合并").pack(pady=10)

    Button(root, text="选择计薪加班文件", command=select_money_file).pack(pady=5)
    Button(root, text="选择调休加班文件", command=select_rest_file).pack(pady=5)
    Button(root, text="合并文件", command=merge_files).pack(pady=20)

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