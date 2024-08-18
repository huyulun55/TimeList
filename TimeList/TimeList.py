#!/usr/bin/env python

import tkinter
from tkinter import messagebox
import time
import threading

root = tkinter.Tk()
root.withdraw()
global orange_data = None
def load_data():
    with open('OrangeList.json', 'r') as f:
        orange_data = json.load(f)

def show_time(task):
    current_time = time.strftime("%H:%M:%S")
    messagebox.showinfo("时间",f"时间：{current_time}\n任务：{task}")

def check_time():
    if orange_data is None:
        messagebox.showinfo("错误", "配置文件错误")
    else:
        time_list = orange_data.get("TimeList")
        
    while True:
        if isinstance(time_list, list):
            for time_point in time_list:
                if time_point.get("TimePoint") == time.strftime("%H:%M:%S"):
                    task = time_point.get("Task")
                    show_time(task)
                    # 避免同一整点多次弹窗
                    time.sleep(60)
                #每秒检查一次
                time.sleep(1)

show_time()
# 在后台线程中运行检查时间的函数
threading.Thread(target=check_time, daemon=True).start()

# 防止脚本退出
root.mainloop()
