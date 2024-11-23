import tkinter,sys,time,threading

root = tkinter.Tk()
root.overrideredirect(True)
root.attributes("-alpha", 0.8)
root.wm_attributes("-topmost", 1)
root.geometry("160x200+1375+200")
tkinter.Label(root, justify="left", font=(None, 12), text="djsf").place(x=0, y=0)

all_y = root.winfo_screenheight()
all_x = root.winfo_screenwidth()
x,y = 0,0
rootalpha = 0.1
is_hide = "right"

def get_pos(event):
    global x,y
    x,y = event.x,event.y

def window_move(event):
    global x,y
    new_x = min(all_x-160, (event.x-x)+root.winfo_x())
    new_y = min(all_y-200, (event.y-y)+root.winfo_y())
    root.geometry("160x200+"+str(new_x)+"+"+str(new_y))

def change_alpha(event):
    global rootalpha
    if rootalpha==0.1:rootalpha=0.8
    else:rootalpha=0.1
    root.attributes("-alpha",rootalpha)

def close(event):
    root.destory()
    sys.exit()

def move_3(a,b,root=root):
    while root.winfo_x()<all_x-40 and is_hide=="right":
        root.geometry("160x200"+str(root.winfo_x()+4)+"+"+str(root.winfo_y()))
        time.sleep(0.001)
    while root.winfo_x()<all_x-160 and is_hide=="left":
        root.geometry("160x200"+str(root.winfo_x()-4)+"+"+str(root.winfo_y()))
        time.sleep(0.001)
    while root.winfo_y()<all_y-200 and is_hide=="up":
        root.geometry("160x200"+str(root.winfo_x())+"+"+str(root.winfo_y()-5))
        time.sleep(0.001)
    while root.winfo_x()<all_y-40 and is_hide=="down":
        root.geometry("160x200"+str(root.winfo_x())+"+"+str(root.winfo_y(+5)))
        time.sleep(0.001)

def move_1(event):
    global is_hide
    if root.winfo_x()>=all_x-160 and str(event.type)=="Leave":is_hide="right"
    elif root.winfo_x()<=all_x-40 and str(event.type)=="Enter" and not is_hide in"updown":is_hide="left"
    elif root.winfo_y()>=all_x-200 and str(event.type)=="Leave":is_hide="down"
    elif root.winfo_y()<=all_x-40 and str(event.type)=="Enter":is_hide="up"
    else:pass
    threading.Tread(target=move_3,args=(root.info_x(),root.winfo_y())).start()

root.bind("<B1-Motion>",window_move)
root.bind("<Button-1>",get_pos)

root.bind("<Double-Button_1>",change_alpha)
root.bind("<Double-button-3>",close)

root.bind("<Leave>",move_1)
root.bind("<Enter>",move_1)

root.mainloop()
