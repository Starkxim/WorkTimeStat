from tkinter import Tk, Menu, ttk, END
import ui.utils.Utils_Functions as uf


def create_main_window():
    """
    创建主窗口。

    创建一个Tkinter主窗口，包含菜单、Treeview、搜索框和按钮，并启动主循环。
    """
    global tree
    root = Tk()
    root.focus_force()
    root.title("工作时间处理工具")
    uf.center_window(root, 1200, 600)

    menu = Menu(root)
    root.config(menu=menu)

    # 创建“附加”菜单
    additional_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="附加", menu=additional_menu)
    additional_menu.add_command(
        label="更新节假日和补班日期", command=uf.Update_holidays
    )

    # 创建“统计”菜单
    stats_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="统计", menu=stats_menu)
    stats_menu.add_command(
        label="每月加班时长", command=lambda: uf.show_monthly_overtime(tree)
    )
    stats_menu.add_command(
        label="加班时长图表", command=lambda: uf.show_overtime_chart(tree)
    )

    # 创建“文件”菜单
    file_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(
        label="选择计薪加班文件", command=lambda: uf.select_money_file(tree)
    )
    file_menu.add_command(
        label="选择调休加班文件", command=lambda: uf.select_rest_file(tree)
    )
    file_menu.add_separator()
    file_menu.add_command(label="合并文件", command=lambda: uf.merge_files(tree))

    # 创建Treeview和滚动条
    frame = ttk.Frame(root)
    frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(frame, columns=10, height=10, show="headings")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")

    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    hsb.pack(side="bottom", fill="x")

    tree.pack(fill="both", expand=True)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # 添加搜索框和按钮
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=10)

    search_label = ttk.Label(search_frame, text="搜索:")
    search_label.pack(side="left")

    def clear_entry(event):
        """
        清空搜索框内容。

        当搜索框被点击时，清空其内容。
        """
        search_entry.delete(0, END)

    search_entry = ttk.Entry(search_frame)
    search_entry.insert(0, "输入搜索关键字")
    search_entry.bind("<Button-1>", clear_entry)
    search_entry.pack(side="left", padx=5)

    search_button = ttk.Button(
        search_frame,
        text="搜索",
        command=lambda: uf.search_tree(tree, search_entry.get()),
    )
    search_button.pack(side="left")

    root.mainloop()


if __name__ == "__main__":
    print("程序应该从main.py启动")
