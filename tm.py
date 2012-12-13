#!/opt/local/python3/bin/python3
#-*- coding:utf-8 -*-

import os, sys

from tkinter import *

PythonVersion = 3
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()
#from tkMessageBox import showinfo
#import time,tkMessageBox
import threading
import time

class AppTk(Tk):
    stop = False
    remain_time_thr  = False
    def __init__(self):
        Tk.__init__(self)

    def destroy(self):
        if self.remain_time_thr != False and self.remain_time_thr.isAlive():
            self.stop = True
            #self.remain_time_thr.join()
        Tk.destroy(self)
    
#窗体设计
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    #time_status_text    = '当前没有时间执行任务'
    now_runtime_allsec  = 0 # 当前执行的总描述
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('番茄计时器')
        self.master.geometry('312x206')
        self.createWidgets()
        self.bg="blue" 
    def createWidgets(self):
        global time_status_text
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.time_historyVar = StringVar(value='')
        self.time_history = Listbox(self.top, listvariable=self.time_historyVar)
        self.time_history.place(relx=0.103, rely=0.466, relwidth=0.772, relheight=0.427)

        self.startbtn = Button(self.top, text='开始', command=self.startbtn_Cmd)
        self.startbtn.place(relx=0.59, rely=0.117, relwidth=0.183, relheight=0.121)
        self.time_numberVar = StringVar(value='25')
        self.time_number = Entry(self.top, text='25', textvariable=self.time_numberVar)
        self.time_number.place(relx=0.359, rely=0.117, relwidth=0.183, relheight=0.121)
     
        self.style.configure('time_status.TLable',anchor='w')
        self.time_status= Label(self.top,text="",style='time_status.TLabel')
        self.time_status.place(relx=0.103, rely=self.testy,relwidth=0.762,relheight=0.121)
       
        self.style.configure('Label1.TLabel',anchor='w')
        self.Label1 = Label(self.top, text='设置时间(分钟)', style='Label1.TLabel')
        self.Label1.place(relx=0.026, rely=0.155, relwidth=0.317, relheight=0.083)

class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    testy=0.311
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
    
    #结束时的任务处理
    def on_over(self):
        if self.master.stop == True :
            return False
        message = "你刚刚成功完成了一个计时任务 , 耗时 %d 分钟"% (self.time_long/60 , )
        #self.macos_message("1","2","3",False)
        self.time_history.insert(END,message)
        self.startbtn['state'] = 'enabled'
        showinfo(title='计时结束',message=message  )
    #更新时间进度 
    def remain_time_update(self):
        self.time_status['text'] = "距离计时结束还有%d 秒" % (self.now_runtime_allsec,)
    
    #计时器。
    def renmain_time_thread(self):

        while self.now_runtime_allsec >0:
            if self.master.stop == True :
                return False
            self.remain_time_update()
            self.now_runtime_allsec = self.now_runtime_allsec-1
            time.sleep(1)     
        self.on_over()
        self.master.remain_time_thr = False
    #点击事件     
    def startbtn_Cmd(self, event=None):
        self.time_long = int(self.time_number.get()) * 60 
        self.now_runtime_allsec = self.time_long
        self.startbtn['state'] = 'disabled'
        #启动一个线程
        self.master.remain_time_thr    = threading.Thread(target = self.renmain_time_thread)
        self.master.remain_time_thr.start()

        #self.t= threading.Timer(self.time_long,self.on_over)
        #self.t.start()

        
        

        pass

if __name__ == "__main__":
    top = AppTk()
    try: 
        Application(top).mainloop()
        top.destroy()
    except RuntimeError as e:
        pass
    except: pass
