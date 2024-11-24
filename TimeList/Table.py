import tkinter,sys,time,threading

# 设置无缓冲区模式方便打印调试
sys.stdout = open(sys.stdout.fileno(), mode='w', buffering = 1)

# 定义全局变量
x = 0
y = 0
height = 200
width = 160
is_hide = None

root = tkinter.Tk()
# 去掉窗口的边框
root.overrideredirect(True)
# 设置窗口的透明度为0.8
root.attributes("-alpha", 0.8)
# 设置窗口总是位于其他窗口之上
root.wm_attributes("-topmost", 1)
# 设置窗口尺寸和初始未知（宽160xp,高200xp,x坐标1375,y坐标200）
root.geometry(f"{width}x{height}+500+300")
# 在窗口的左上角放一个标签，显示文本
tkinter.Label(root, justify="left", font=(None, 12), text="djsf").place(x=0, y=0)
# 获取屏幕长度
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

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
    root.attributes("-alpha", 0.1 if alpha == 0.8 else 0.8)

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
    elif is_hide == "left" and current_x > - 140:
        root.geometry(f"{width}x{height}+{current_x - step_x}+{current_y}")
        root.after(10, hide_window, step_x, step_y)
    # 向下隐藏
    elif is_hide == "down" and current_y < screen_height - 20:
        root.geometry(f"{width}x{height}+{current_x}+{current_y + step_y}")
        root.after(10, hide_window, step_x, step_y)
    # 向上隐藏
    elif is_hide == "up" and current_y > - 180:
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
    # 上隐藏向下显示（5是边缘值）
    elif is_hide == "down" and current_y > screen_height - height + 5:
        root.geometry(f"{width}x{height}+{current_x}+{current_y - step_y}")
        root.after(10, show_window, step_x, step_y)
    # 下隐藏向上显示（5是边缘值）
    elif is_hide == "up" and current_y < 0 - 5:
        root.geometry(f"{width}x{height}+{current_x}+{current_y + step_y}")
        root.after(10, show_window, step_x, step_y)

def hide_check(event):
    global is_hide
    # 检测隐藏条件
    if root.winfo_x() >= screen_width - 160 - 40:
        is_hide = "right"
        hide_window(4, 0)
    elif root.winfo_x() <= 40:
        is_hide = "left"
        hide_window(4, 0)
    elif root.winfo_y() >= screen_height - 200 - 40:
        is_hide="down"
        hide_window(0, 4)
    elif root.winfo_y() <= 40:
        is_hide="up"
        hide_window(0, 4)
    else:
        is_hide = None
        return

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
