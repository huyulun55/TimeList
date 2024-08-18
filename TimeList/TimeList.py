

import tkinter as tk
import tkinter import messagebox
import time

#创建主窗口
root = tk.Tk()
#隐藏主窗口
root.withdraw()

#显示弹窗
messagebox.showinfo("时间表", "现在是？点，现在的任务是？")

#延时3秒
time.sleep(3)

#关闭窗口
root.destory()
