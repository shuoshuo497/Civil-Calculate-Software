import tkinter as tk
from tkinter import messagebox


# 假设您之前已经实现了以下两个函数
def plot_node_coordinates():
    # 这里是结点坐标作图的代码
    messagebox.showinfo("节点坐标作图", "这里是结点坐标作图的功能")


def assemble_rods():
    # 这里是杆件拼装作图的代码
    messagebox.showinfo("杆件拼装作图", "这里是杆件拼装作图的功能")


# 创建主界面
def create_main_window():
    # 创建主窗口
    root = tk.Tk()
    root.title("主界面")
    root.geometry("300x200")

    # 创建并放置两个按钮
    btn_node_coordinates = tk.Button(root, text="结点坐标作图", command=plot_node_coordinates)
    btn_node_coordinates.pack(pady=20)

    btn_assemble_rods = tk.Button(root, text="杆件拼装作图", command=assemble_rods)
    btn_assemble_rods.pack(pady=20)

    # 运行主循环
    root.mainloop()


# 运行程序
if __name__ == "__main__":
    create_main_window()
