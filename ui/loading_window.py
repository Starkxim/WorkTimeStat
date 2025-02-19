import tkinter as tk
from ui.utils.Utils_Functions import center_window

def show_loading_screen():
    loading_root = tk.Tk()
    loading_root.title("正在启动")
    center_window(loading_root, 300, 100)
    label = tk.Label(loading_root, text="正在启动，请稍候...", font=("", 20))
    label.pack(pady=20)
    loading_root.after(3000, loading_root.destroy)  # 显示3秒后关闭加载窗口
    loading_root.mainloop()