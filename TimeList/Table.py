import tkinter,sys,time,threading

root = tkinter.Tk()
# 去掉窗口的边框
root.overrideredirect(True)
# 设置窗口的透明度为0.8
root.attributes("-alpha", 0.8)
# 设置窗口总是位于其他窗口之上
root.wm_attributes("-topmost", 1)
# 设置窗口尺寸和初始未知（宽160xp,高200xp,x坐标1375,y坐标200）
root.geometry("160x200+1375+200")
# 在窗口的左上角放一个标签，显示文本
tkinter.Label(root, justify="left", font=(None, 12), text="djsf").place(x=0, y=0)

all_y = root.winfo_screenheight()
all_x = root.winfo_screenwidth()
x,y = 0,0
rootalpha = 0.1
is_hide = "right"

# 记录鼠标点击时的相对位置
def get_pos(event):
    global x,y
    x,y = event.x,event.y

def window_move(event):
    global x,y
    # 限制x坐标在屏幕范围内
    new_x = max(0, min(all_x-160, (event.x-x)+root.winfo_x()))
    # 限制y坐标在屏幕范围内
    new_y = max(0, min(all_y-200, (event.y-y)+root.winfo_y()))
    # 更新窗口的位置
    root.geometry("160x200+"+str(new_x)+"+"+str(new_y))

def change_alpha(event):
    global rootalpha
    # 鼠标左键双击在两种透明度之间切换
    if rootalpha ==0.1:rootalpha=0.8
    else:rootalpha=0.1
    # 更新透明度
    root.attributes("-alpha",rootalpha)

def close(event):
    # 关闭窗口
    root.destroy()
    # 退出程序
    sys.exit()

def move_3(a,b,root=root):
    global is_hide
    # 向右隐藏
    if is_hide == "right":
        while root.winfo_x() > all_x - 40:
            root.geometry(f"160x200+{root.winfo_x() - 4}+{root.winfo_y()}")
            time.sleep(0.01)
    # 向左隐藏
    if is_hide == "left":
        while root.winfo_x() < - 160:
            root.geometry(f"160x200+{root.winfo_x() + 4}+{root.winfo_y()}")
            time.sleep(0.01)
    # 向下隐藏
    if is_hide == "down":
        while root.winfo_y() > all_y - 40:
            root.geometry(f"160x200+{root.winfo_x()}+{root.winfo_y() - 4}")
            time.sleep(0.01)
    # 向上隐藏
    if is_hide == "up":
        while root.winfo_t() < 200:
            root.geometry(f"160x200+{root.winfo_x()}+{root.winfo_y() + 4}")
            time.sleep(0.01)

def move_1(event):
    global is_hide
    # 鼠标离开时隐藏的逻辑
    if root.winfo_x() >= all_x - 160 and str(event.type) == "Leave":
        is_hide = "right"
    elif root.winfo_x() <= 0 and str(event.type) == "Leave":
        is_hide = "left"
    elif root.winfo_y() >= all_y - 200 and str(event.type) == "Leave":
        is_hide="down"
    elif root.winfo_y() <= 0 and str(event.type)=="Leave":
        is_hide="up"
    else:
        return
    # 启动线程执行隐藏逻辑
    threading.Thread(target=move_3,args=(root.winfo_x(),root.winfo_y())).start()

# 绑定鼠标左键拖动事件
root.bind("<B1-Motion>",window_move)
# 绑定鼠标左键按下事件
root.bind("<Button-1>",get_pos)

# 绑定鼠标左键双击切换透明度
root.bind("<Double-Button-1>",change_alpha)
# 绑定鼠标右键双击关闭窗口
root.bind("<Double-Button-3>",close)

# 鼠标移出窗口
root.bind("<Leave>",move_1)
# 鼠标移入窗口
root.bind("<Enter>",move_1)

root.mainloop()