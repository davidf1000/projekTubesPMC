"""
Program Interface 
Kelompok 17
David Fauzi     / 13218043
Elang Aditya    / 13218041 
Putri Yulianti  / 18318004 
Lucas Valentino / 13218042 

Keterangan : Program GUI menggunakan modul TKinter, masukan input akan disave pada file 
netlist.txt dan program akan meng-compile dan run program mainprog.c menggunakan modul OS .
Output berupa data CSV akan di plot menggunakan modul Pandas dan Matplotlib 
"""

#Import Modul
from tkinter import *
# from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import ttk
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
#initiate master window
window=Tk()
window.title("RC Simulator")
window.geometry("700x800")
# Frame 1 (Intro) amd Frame 2 (Main)
print("Starting Program")
#Fungsi untuk switch frame 
def raise_frame(frame):
    frame.tkraise()
#initialize frame
f1 = Frame(window)
f2 = Frame(window)
#initialize grid 
for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')
#constant
grid3_width=20
grid3_heigth=3
grid3_front_size=15
gridintro_heigth=8

# Tampilan Intro Frame
#Intro middle
label_Intro=Label(f1,font=("Arial Bold",grid3_front_size+3),text="Welcome to RC Simulator",height=gridintro_heigth,width=grid3_width)
label_Intro.grid(column=1,row=0)
#Filler intro column 0 1 
label_Intro1=Label(f1,font=("Arial",grid3_front_size),text=" ",height=gridintro_heigth,width=grid3_width)
label_Intro2=Label(f1,font=("Arial",grid3_front_size),text=" ",height=gridintro_heigth,width=grid3_width)
label_Intro1.grid(column=0,row=0)
label_Intro2.grid(column=2,row=0)
#scroll text to show team member list
scroll=scrolledtext.ScrolledText(f1,width=25,height=7,font=("Arial",grid3_front_size))
scroll.grid(column=1,row=1)

#Instruction
strintro="Instruction :\n\n1. Click Start\n2.Input all component values\n3. Input simulation stop time\n4. Choose Plot Option \n5. Click simulate"
label_Ins=Label(f1,justify="center",font=("Arial",grid3_front_size),text=strintro,height=gridintro_heigth,width=grid3_width+5)
label_Ins.grid(column=1,row=4)
# callback function to print all team member and nim 
def inputtext():
    scroll.insert(INSERT,"Kelompok 17 ...\n")
    f1.after(500,second)
def second():
    scroll.insert(INSERT,"David Fauzi       / 13218043\n")
    f1.after(500,third)

def third():
    scroll.insert(INSERT,"Elang Aditya      / 13218041 \n")
    f1.after(500,fourth)

def fourth():
    scroll.insert(INSERT,"Putri Yulianti      / 18318004 \n")
    f1.after(500,fifth)
def fifth():
    scroll.insert(INSERT,"Lucas Valentino / 13218042 \n")

#Button , when pressed frame changed to main frame
btn_Start=Button(f1,font=("Arial",grid3_front_size),text="Start",bd=3,command=lambda:raise_frame(f2) )
btn_Start.grid(column=1,row=3,pady=10)


# Main Frame
# Top text
label1=Label(f2,font=("Arial",grid3_front_size),text="Input Component Value",height=grid3_heigth)
label1.grid(column=1,row=0)

#Resistor Section
#Label
label_Resistor=Label(f2,font=("Arial",grid3_front_size),text="Resistor\nValue",width=grid3_width,height=grid3_heigth)
label_Resistor.grid(column=1,row=1)
#Entry
input_Resistor=Entry(f2,state="normal",width=10)
input_Resistor.focus()
input_Resistor.grid(column=1,row=2)
#Combobox
comboRes = ttk.Combobox(f2,width=5)
comboRes['values']=('Ω','KΩ','MΩ')
comboRes.current(1)
comboRes.grid(column=1,row=3,pady=4)

#DC Voltage Section
#Label
label_DC=Label(f2,font=("Arial",grid3_front_size),text="DC\nValue",width=grid3_width,height=grid3_heigth)
label_DC.grid(column=0,row=4)
#Entry
input_DC=Entry(f2,state="normal",width=10)
input_DC.grid(column=0,row=5)
input_DC.focus()
#ComboBox
comboDC = ttk.Combobox(f2,width=5)
comboDC['values']=('V','KV','MV')
comboDC.current(0)
comboDC.grid(column=0,row=6,pady=4)


#Capacitor Section
#Label
label_Cap=Label(f2,font=("Arial",grid3_front_size),text="Cap\nValue",width=grid3_width,height=grid3_heigth)
label_Cap.grid(column=2,row=4)
#Entry
input_Cap=Entry(f2,state="normal",width=10)
input_Cap.grid(column=2,row=5)
input_Cap.focus()
#Combobox
comboCap = ttk.Combobox(f2,width=5)
comboCap['values']=('nF','uF')
comboCap.current(1)
comboCap.grid(column=2,row=6,pady=4)
#Circuit Image
img = PhotoImage(file = "rcnew.png")
label_RC=Label(f2,image=img,width=250)
label_RC.grid(column=1,row=7,rowspan=1)


#Callback Function , get entry input lalu diconvert sesuai satuan yang dipilih combobox
def proc_res():
    res=float(input_Resistor.get())
    mark=comboRes.get()
    if(mark=="Ω"):
        res*=1
    elif(mark=="KΩ"):
        res*=1e3
    elif(mark=="MΩ"):
        res*=1e6
    return res
def proc_DC():
    dc=float(input_DC.get())
    mark=comboDC.get()
    if(mark=="V"):
        dc*=1
    elif(mark=="KV"):
        dc*=1e3
    elif(mark=="MV"):
        dc*=1e6
    return dc
def proc_cap():
    cap=float(input_Cap.get())
    mark=comboCap.get()
    if(mark=="nF"):
        cap*=1e-9
    elif(mark=="uF"):
        cap*=1e-6
    return cap
def proc_time():
    time=float(input_time.get())
    mark=comboTime.get()
    if(mark=="S"):
        time*=1
    elif(mark=="mS"):
        time*=1e-3
    return time   

#write to txt netlist.txt
def writetoTxt(res,dc,cap,time):
    """
    contoh format :
        2 3
    v 0 1 10
    r 1 2 20000
    c 2 0 0.00001
    2.5
    """
    text=open("netlist.txt","w+")
    #Struktur node konstan karena rangkaian pre-determined yaitu rangkaian RC 
    text.write("2 3\n")
    text.write("v 0 1 "+str(dc)+"\n")
    text.write("r 1 2 "+str(res)+"\n")
    text.write("c 2 0 "+str(cap)+"\n")
    text.write(str(time)+"\n")
    text.close()

#Fungsi untuk memulai proses perhitungan simulasi
def calc():
    #Kalau semua input belum keisi, akan muncul pesan error pada label 
    try:
        res=proc_res()
        dc=proc_DC()
        cap=proc_cap()
        time=proc_time()
        writetoTxt(res,dc,cap,time)
        print("Input User :\n")
        print("Resistor :"+str(res))
        print("DC Source :"+str(dc))
        print("Kapasitor :"+str(cap))
        print("Stop Time :"+str(time))
        print("\n")
        print("Data telah di simpan di netlist.txt")
        bar2()
    except:
        label_Process.configure(text="Please fill all components\nvalue first...")

#Fungsi callback untuk tampilan progress bar
def bar2():
    label_Process.configure(text="Processing.....")
    bar['value']=20
    f2.after(100,bar3)
def bar3():
    bar['value']=40
    f2.after(100,bar4)
def bar4():
    #Compiling program C (Bisa dihapus kalau program C udah tidak ada revisi)
    label_Process.configure(text="Running C Code.....")
    os.system("gcc -o run ../programc/mainprog.c ../programc/matriks.c ")
    bar['value']=60
    f2.after(500,bar5)

def bar5():
    bar['value']=80
    #run program C
    os.system('run')
    print("Kode C telah di compile dan di run")
    f2.after(500,bar6)

def bar6():
    bar['value']=100
    #Progress 100% , tampilkan plot 
    updateproc()
    showplot()

#update text process
def updateproc():
    label_Process.configure(text="Success, Showing plot...")
    print("Menampilkan Plot dari output.csv")

#callback function untuk membaca output.csv dan menampilkan plot 
def showplot():
    data = pd.read_csv('output.csv',encoding='utf8')
    x=data['time']
    y=data['v_1']
    z=data['v_2']
    p=data['i_1']
    r=data['res']
    ptot=data['ptot']
    pres=data['pres']
    pcap=data['pcap']

    #plot
    #Voltage , menampilkan sesuai checkbox user
    if((vcc_state.get()) or (cap_state.get()) or (res_state.get())):
        fig=plt.figure()
        if(vcc_state.get()):
            plt.plot(x,y,label="Source Voltage",linewidth=2.5)
        if(cap_state.get()):
            plt.plot(x,z,label="Cap Drop Voltage",linewidth=2)
        if(res_state.get()):
            plt.plot(x,r,label="Res Drop Voltage",linewidth=2)  
        fig.suptitle('Voltage Plot', fontsize=20)
        plt.xlabel('Time (S)', fontsize=18)
        plt.ylabel('Voltage (V)', fontsize=16)
        plt.grid(True)
        plt.legend()
    #Arus
    if(curr_state.get()):
        fig2=plt.figure()
        plt.plot(x,p,label="Current",linewidth=2)
        fig2.suptitle('Current Plot', fontsize=20)
        plt.xlabel('Time (S)', fontsize=18)
        plt.ylabel('Current (mA)', fontsize=16)
        plt.legend()
        plt.grid(True)
    # Daya
    if(powertot_state.get() or powerres_state.get() or powercap_state.get() ):
        fig3=plt.figure()
        if(powertot_state.get()):
            plt.plot(x,ptot,label="Supply Power",linewidth=2.5)
        if(powerres_state.get()):
            plt.plot(x,pres,label="Res Power",linewidth=2)    
        if(powercap_state.get()):
            plt.plot(x,pcap,label="Cap Power",linewidth=2)
        fig3.suptitle('Power Plot', fontsize=20)
        plt.xlabel('Time (S)', fontsize=18)
        plt.ylabel('Power (mW)', fontsize=16)
        plt.legend()
        plt.grid(True)
    #Kalau tidak ada yang di check, muncul pesan error pada label 
    if (powertot_state.get() or powerres_state.get() or powercap_state.get() or curr_state.get() or (vcc_state.get()) or (cap_state.get()) or (res_state.get())): 
        plt.show()
    else:
        label_Process.configure(text="Nothing to plot..\nCheck At least 1 Plot option")

        
#Time 
label_time=Label(f2,font=("Arial",grid3_front_size),text="Stop Time :",height=grid3_heigth-2)
label_time.grid(column=1,row=8)

input_time=Entry(f2,state="normal",width=10)
input_time.grid(column=1,row=9)
input_time.focus()

comboTime = ttk.Combobox(f2,width=5)
comboTime['values']=('mS','S')
comboTime.current(0)
comboTime.grid(column=1,row=10,pady=8)
#When pressed callback to function
btn_Calculate=Button(f2,font=("Arial",grid3_front_size+5),text="Simulate",bd=3,command=calc)
btn_Calculate.grid(column=1,row=11,pady=10)
#Bar
bar = Progressbar(f2, length=200)
bar['value'] = 2
bar.grid(column=1,row=12)
#sucess 
label_Process=Label(f2,font=("Arial",grid3_front_size),text=" ",height=grid3_heigth)
label_Process.grid(column=1,row=13)
# Checkbox 

# VCC 
vcc_state = BooleanVar()
vcc_state.set(True) #set check state
vcc_chk = Checkbutton(f2, text='DC Supply',font=("Arial",grid3_front_size), var=vcc_state)
vcc_chk.grid(column=0, row=10)

# Current
curr_state = BooleanVar()
curr_state.set(True) #set check state
curr_chk = Checkbutton(f2, text='Current',font=("Arial",grid3_front_size), var=curr_state)
curr_chk.grid(column=0, row=13)

#  Capacitor Voltage Drop
cap_state = BooleanVar()
cap_state.set(True) #set check state
cap_chk = Checkbutton(f2, text='Cap Voltage Drop',font=("Arial",grid3_front_size), var=cap_state)
cap_chk.grid(column=0, row=11)

# Resistor voltage drop
res_state = BooleanVar()
res_state.set(True) #set check state
res_chk = Checkbutton(f2, text='Res Voltage Drop',font=("Arial",grid3_front_size), var=res_state)
res_chk.grid(column=0, row=12)

# tot power
powertot_state = BooleanVar()
powertot_state.set(True) #set check state
powertot_chk = Checkbutton(f2, text='Supply Power',font=("Arial",grid3_front_size), var=powertot_state)
powertot_chk.grid(column=2, row=11)

# res power
powerres_state = BooleanVar()
powerres_state.set(True) #set check state
powerres_chk = Checkbutton(f2, text='Res Power',font=("Arial",grid3_front_size), var=powerres_state)
powerres_chk.grid(column=2, row=12)

# cap power
powercap_state = BooleanVar()
powercap_state.set(True) #set check state
powercap_chk = Checkbutton(f2, text='Cap Power',font=("Arial",grid3_front_size), var=powercap_state)
powercap_chk.grid(column=2, row=13)



#dont change

#pertama raise frame intro dahulu
raise_frame(f1)
inputtext()
window.mainloop()