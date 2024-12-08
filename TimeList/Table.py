"""
v3.2版本 
功能：悬浮停靠时间表，支持向上向左向右停靠，根据配置文件现实时间表
BUG: 向下隐藏有BUG，只要运行select_file函数就会出现，疑似和任务栏有关
"""
import os
import sys
import json
import time
import tkinter
import threading
from tkinter import messagebox, simpledialog

# 定义全局变量
x = 0
y = 0
height = 400
width = 320
is_hide = None
data = None
scheule = []
root = tkinter.Tk()
screen_height = 0 
screen_width = 0

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

def initialize_window():
    global root, screen_height, screen_width
    # 隐藏窗口
    root.withdraw()
    # 去掉窗口的边框
    root.overrideredirect(True)
    # 设置窗口的透明度为0.8
    root.attributes("-alpha", 0.8)
    # 设置窗口总是位于其他窗口之上
    root.wm_attributes("-topmost", 1)
    # 获取屏幕长度
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    # 设置窗口尺寸和初始未知（宽160xp,高200xp,x坐标1375,y坐标200）
    root.geometry(f"{width}x{height}+{screen_width-width}+200")

def load_data(filename):
    global data, schedule
    try:
        # 获取程序所在的目录
        if getattr(sys, 'frozen', False):  # 检查是否是打包后的应用
            # 如果是打包后的应用，sys.argv[0] 会是 .exe 文件的路径
            exe_dir = os.path.dirname(sys.argv[0])  # 获取 .exe 文件所在的目录
        else:
            # 在开发环境中，使用当前脚本所在的目录
            exe_dir = os.path.dirname(os.path.abspath(__file__))

        # 构造配置文件的完整路径
        file_path = os.path.join(exe_dir, filename)
        with open(file_path, 'r', encoding = 'utf-8') as f:
            data = f.readlines()
        data = ''.join(data)
        #解析时间表数据，假设每行都是“时间 - 事项”
        schedule = []
        for line in data.splitlines():
            time_point, task = line.split(" - ")
            schedule.append({"time:" time_point.strip(), "task":task.strip()})
    except FileNotFoundError:
        messagebox.showerror("错误", "配置文件未找到")
        root.quit()
    except json.JSONDecodeError:
        messagebox.showerror("错误", "配置文件格式错误")
        root.quit()
    except UnicodeDecodeError:
        messagebox.showerror("错误", "配置文件编码不是UTF-8无法解码")
        root.quit()

# 选择配置文件（时间表）
def select_file():
    file_choice = simpledialog.askstring("选择时间列表", "请输入希望加载的时间表名称(overtime, bath, leisure, swim):")
    if file_choice == "overtime":
        load_data("OvertimeList.txt")
    elif file_choice == "bath":
        load_data("BathList.txt")
    elif file_choice == "leisure":
        load_data("LeisureList.txt")
    elif file_choice == "swim":
        load_data("SwimList.txt")
    else:
        messagebox.showerror("错误", "无效的配置文件名")
        root.quit()
    # 显示窗口
    root.deiconify()
    # 初始显示时间表
    update_schedule()

# 更新窗口中的时间表
def update_schedule():
    current_time = time.strftime("%H:%M")
    # 设置标志位
    bool flag = false
    for index, entry in enumerate(schedule):
        # 根据时间匹配当前时间
        if entry['time'] == current_time
            flag = true

    if flag == true
        for widget in root.winfo_children():
            # 清除当前窗口中的所有组件
            widget_destory()

        for index, entry in enumerate(schedule):
            # 根据时间匹配当前时间
            color "red" if entry['time'] == current_time else "black"
            tkinter.Label(root, justify="left", font(None, 12), text=f"{entry['time']} - {entry['task']}", fg=color).place(x=0, y=index * 30)
        flag = false

# 定时检查当前时间并更新窗口内容
def check_time():
    update_schedule()
    # 每分钟检查一次
    root.after(60000, chekc_time)

# 记录鼠标点击时的相对位置
def get_pos(event):
    global x,y
    x,y = event.x,event.y

# 限制窗口拖动范围
def window_move(event):
    global x,y
    # 限制x坐标在屏幕范围内（5是边缘值）
    new_x = max(-5, min(screen_width - width + 5, (event.x - x) + root.winfo_x()))
    # 限制y坐标在屏幕范围内（5是边缘值）
    new_y = max(-5, min(screen_height - height + 5, (event.y - y) + root.winfo_y()))
    # 更新窗口的位置
    root.geometry(f"{width}x{height}+{new_x}+{new_y}")

# 切换透明度
def change_alpha(event):
    # 鼠标左键双击在两种透明度之间切换
    alpha = root.attributes("-alpha")
    # 更新透明度
    root.attributes("-alpha", 0.3 if alpha == 0.8 else 0.8)

# 关闭窗口
def close(event):
    # 关闭窗口
    root.destroy()
    # 退出程序
    sys.exit()

# 贴边隐藏
def hide_window(step_x, step_y):
    global is_hide
    current_x = root.winfo_x()
    current_y = root.winfo_y()
    # 向右隐藏
    if is_hide == "right" and current_x < screen_width - 20:
        root.geometry(f"{width}x{height}+{current_x + step_x}+{current_y}")
        root.after(10, hide_window, step_x, step_y)
    # 向左隐藏
    elif is_hide == "left" and current_x > - width + 20:
        root.geometry(f"{width}x{height}+{current_x - step_x}+{current_y}")
        root.after(10, hide_window, step_x, step_y)
    # 向下隐藏(BUG)
    elif is_hide == "down" and current_y < screen_height - 20:
         root.geometry(f"{width}x{height}+{current_x}+{current_y + step_y}")
         root.after(10, hide_window, step_x, step_y)
    # 向上隐藏
    elif is_hide == "up" and current_y > - height + 20:
        root.geometry(f"{width}x{height}+{current_x}+{current_y - step_y}")
        root.after(10, hide_window, step_x, step_y)

# 显示窗口
def show_window(step_x, step_y):
    global is_hide
    current_x = root.winfo_x()
    current_y = root.winfo_y()
    # 右隐藏向左显示（5是边缘值）
    if is_hide == "right" and current_x > screen_width - width + 5:
        root.geometry(f"{width}x{height}+{current_x - step_x}+{current_y}")
        root.after(10, show_window, step_x, step_y)
    # 左隐藏向右显示（5是边缘值）
    elif is_hide == "left" and current_x < 0 - 5:
        root.geometry(f"{width}x{height}+{current_x + step_x}+{current_y}")
        root.after(10, show_window, step_x, step_y)
    # 下隐藏向上显示（5是边缘值）
    elif is_hide == "down" and current_y > screen_height - height + 5:
         root.geometry(f"{width}x{height}+{current_x}+{current_y - step_y}")
         root.after(10, show_window, step_x, step_y)
    # 上隐藏向下显示（5是边缘值）(BUG)
    elif is_hide == "up" and current_y < 0 - 5:
       root.geometry(f"{width}x{height}+{current_x}+{current_y + step_y}")
       root.after(10, show_window, step_x, step_y)

def hide_check(event):
    global is_hide
    # 检测隐藏条件
    if root.winfo_x() >= screen_width - width - 1:
        is_hide = "right"
        hide_window(4, 0)
    elif root.winfo_x() <= 1:
        is_hide = "left"
        hide_window(4, 0)
    elif root.winfo_y() >= screen_height - height - 1:
        is_hide="down"
        hide_window(0, 4)
    elif root.winfo_y() <= 1:
        is_hide="up"
        hide_window(0, 4)
    else:
        is_hide = None

def show_check(event):
    global is_hide
    if is_hide == "right":
        show_window(4, 0)
    elif is_hide == "left":
        show_window(4, 0)
    elif is_hide == "down":
        show_window(0, 4)
    elif is_hide == "up":
        show_window(0, 4)

if __name__ == "__main__":
    initialize_window()
    select_file()
    root.after(100, check_time)
    # 绑定鼠标左键拖动事件
    root.bind("<B1-Motion>", window_move)
    # 绑定鼠标左键按下事件
    root.bind("<Button-1>", get_pos)
    # 绑定鼠标左键双击切换透明度
    root.bind("<Double-Button-1>", change_alpha)
    # 绑定鼠标右键双击关闭窗口
    root.bind("<Double-Button-3>", close)
    # 鼠标移出窗口
    root.bind("<Leave>", hide_check)
    # 鼠标移入窗口
    root.bind("<Enter>", show_check)

    root.mainloop()
