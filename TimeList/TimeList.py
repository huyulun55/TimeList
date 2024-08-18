#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
import time
import threading

def show_time():
    root = tk.Tk()
    root.withdraw()
    current_time = time.strftime("%H:%M:%S")
    messagebox.showinfo("时间",f"{current_time}")
    root.destory()

def check_time():
    while True:
        current_time = time.strftime("%H:%M:%S")
        point_time = "15:00:00"
        if current_time == point_time:
            show_time()
            # 避免同一整点多次弹窗
            time.sleep(60)
        # 每秒检查一次
        time.sleep(1)

# 在后台线程中运行检查时间的函数
threading.Thread(target=check)time, deamon=True).start()

# 防止脚本退出
tk.mainloop()
