import sys
import DocxReader as reader
import tkinter
from os import listdir
from os.path import join,isfile
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image

##def resize_image(event,image2):
##    new_width = event.width
##    new_height = event.height
##    image = image2.resize((new_width, new_height))
##    photo = ImageTk.PhotoImage(image)
##    background_label.config(image = photo)
##    background_label.image = photo #avoid garbage collection

#def clicked2(txt):
#    dir=tkinter.filedialog.askdirectory()
#    txt.insert(20,dir)

#def text_input(txt):
#    input = txt.get()
#    if (input !=""):
#        onlyfiles = [f for f in listdir(input) if isfile(join(input, f))]
#        print(onlyfiles)
#    else:
#        messagebox.showinfo("Error", "please write the directory")

def start_scanning(files,directory,bt3):
    for file in files:
        reader.scan_docx(join(directory,file))
        print(reader.get_sentence_list())
        print("\n")
    bt3.config(state="normal")
