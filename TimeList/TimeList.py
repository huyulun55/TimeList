#!/usr/bin/env python

import os
import json
import time
import tkinter
import threading
from tkinter import messagebox, simpledialog

root = tkinter.Tk()
root.withdraw()
data = None

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_data(filename):
    global data
    try:
        file_path = os.path.join(script_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("错误", "配置文件未找到")
        root.destroy()
    except json.JSONDecodeError:
        messagebox.showerror("错误", "配置文件格式错误")
        root.destroy()
    except UnicodeDecodeError:
        messagebox.showerror("错误", "配置文件编码不是UTF-8无法解码")

def show_time(task):
    current_time = time.strftime("%H:%M:%S")
    messagebox.showinfo("时间",f"时间：{current_time}\n任务：{task}")

def check_time():
    global data
    
    if data is None:
        messagebox.showinfo("错误", "配置文件错误")
        return

    time_list = data.get("TimeList", [])
        
    while True:
        current_time = time.strftime("%H:%M:%S")
        if isinstance(time_list, list):
            for time_point in time_list:
                if time_point.get("TimePoint") == current_time:
                    task = time_point.get("Task")
                    show_time(task)
                    # 避免同一整点多次弹窗
                    time.sleep(60)
                    break;
        # 每秒检查一次
        time.sleep(1)

def select_file():
    # 弹出选择框
    file_choice = simpledialog.askstring("选择时间列表", "请输入希望加载的时间列表名（orange, green, red）:")
    if file_choice == "orange":
        load_data("OrangeList.json")
    elif file_choice == "green":
        load_data("GreenList.json")
    elif file_choice == "red":
        load_data("RedList.json")
    else:
        messagebox.showerror("错误", "无效的配置文件名")
        root.destroy()

if __name__ == "__main__":
    select_file()
    # 在后台线程中运行检查时间的函数
    threading.Thread(target=check_time, daemon=True).start()
    # 防止脚本退出
    root.mainloop()
