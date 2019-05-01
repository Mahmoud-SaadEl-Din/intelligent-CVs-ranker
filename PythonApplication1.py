from functions import *
#import sys
#import tkinter
#from tkinter import filedialog
#from tkinter import messagebox
#from PIL import ImageTk,Image
#from time import sleep


def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = image3.resize((new_width, new_height))
    image_n = image2.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    photo2 = ImageTk.PhotoImage(image_n)
    background_label2.config(image = photo)
    background_label2.image = photo #avoid garbage collection
    background_label.config(image = photo2)
    background_label.image = photo2 #avoid garbage collection

def finish():
    window.destroy()


def clicked2():
    txt1.delete(0,'end')
    dir=tkinter.filedialog.askdirectory()
    txt1.insert(0,dir) #index???

def text_input():
    input = txt1.get()
    if (input !=""):
        onlyfiles = [f for f in listdir(input) if isfile(join(input, f))]
        print(onlyfiles)
        window.withdraw()
        window2.wm_deiconify()
        start_scanning(onlyfiles,input,btn3)
        #enable_function()
    else:
        messagebox.showinfo("Error", "please write the directory")

#def enable_function():
#    #for i in range(20):
#    #    sleep(0.5)
#    btn3.config(state="normal")


window=tkinter.Tk()
window.geometry('500x500')
window.title("CV Ranker")
window.iconbitmap(r'C:\Users\tarek\source\repos\PythonApplication1\PythonApplication1\CV_Hunter_MaroonBG.ico')
window.resizable(0,0)
image2=Image.open('C:\\Users\\tarek\\source\\repos\\PythonApplication1\\PythonApplication1\\technology_resume-100690687-large.jpg')
image1 = ImageTk.PhotoImage(image2)
background_label = tkinter.Label(window, image=image1)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
lbl=tkinter.Label(window,text="Enter CVs Directory",font=("Arial",14),bg="white")
lbl.grid(column=0,row=0)
txt1=tkinter.Entry(window,width=55);
txt1.place(x=0,y=30);
txt1.focus()
btn1=tkinter.Button(window,text="Browse",command=clicked2)
btn1.place(x=350,y=30)
btn2=tkinter.Button(window,text="Start Scanning",fg="blue",width=30,font=28,command=text_input)
btn2.place(x=80,y=400)
##########################################################################################################
window2=tkinter.Toplevel(window)
window2.geometry('500x300')
window2.resizable(0,0)
window2.withdraw()
window2.title("Scanning Cvs")
window2.iconbitmap(r'C:\Users\tarek\source\repos\PythonApplication1\PythonApplication1\CV_Hunter_MaroonBG.ico')
image3=Image.open('C:\\Users\\tarek\\source\\repos\\PythonApplication1\\PythonApplication1\\CTA_scan_your_resume-03-02.png')
image4 = ImageTk.PhotoImage(image3)
background_label2 = tkinter.Label(window2, image=image4)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)
background_label2.bind('<Configure>', resize_image)
btn3=tkinter.Button(window2,text="Finish",fg="blue",width=10,font=28,command=finish)
btn3.place(x=200,y=250)
btn3.config(state="disable");
window.mainloop()
