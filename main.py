import tkinter as tk
from tkinter import messagebox
from ui.main_window import create_main_window

def show_loading_screen():
    loading_root = tk.Tk()
    loading_root.title("正在启动")
    loading_root.geometry("300x100")
    label = tk.Label(loading_root, text="正在启动，请稍候...", font=("", 20))
    label.pack(pady=20)
    loading_root.after(3000, loading_root.destroy)  # 显示3秒后关闭加载窗口
    loading_root.mainloop()

if __name__ == "__main__":
    show_loading_screen()
    create_main_window()