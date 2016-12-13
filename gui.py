#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFileDialog
import base64


# You can test your code with this gui as soon as you
# have implemented the missing sections of the template
# file. 

# change this if you renamed the template
# try:
#     import template as sl
# except:
#     pass
# 
# try:
#     import solution as sl
# except:
#     pass

import template as sl

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Project")

        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button1 = Button(self, text="Embed", command=self.embed, width=10)
        self.button1.grid(row=1,column=0)
        self.button2 = Button(self, text="Extract", command=self.extract)
        self.button2.grid(row=1,column=1)
        self.button3 = Button(self, text="Show", command=self.show)
        self.button3.grid(row=1,column=2)

        self.text1 = Text(self)
        self.text1.insert(END, "Insert some text here...")
        self.text1.grid(row=2,column=0, columnspan=3)

    def embed(self):      
        filename = tkFileDialog.askopenfilename()
        if filename == "":
            return
        img = sl.openimage(filename)
        text = self.text1.get(1.0, END + '-1c')
        text = base64.b64encode(text.encode('utf8'))

        img_out = sl.embed(text, img)
        filenameout = tkFileDialog.asksaveasfilename()
        if filenameout == "":
            return

        sl.saveimage(img_out, filenameout)

    
    def extract(self):
        filename = tkFileDialog.askopenfilename()
        if filename == "":
            return
        img = sl.openimage(filename)
        text = sl.extract(img)
        text = base64.b64decode(text)
        if text == None:
            text = "Nothing found"
        self.text1.delete(1.0, END)
        self.text1.insert(END, text)

    def show(self):
        filename = tkFileDialog.askopenfilename()
        if filename == "":
            return
        img = sl.openimage(filename)
        sl.showimage(img)

        print("Max. (chr) storage size in image:", self.storagesize(img))

    def storagesize(self, image):
        return int(float(2)/3 * (image.size[0] * image.size[1] * 3 // 8 - len(sl.addmagicstring(""))))

def main():
    MyFrame().mainloop()

if __name__ == "__main__":
    main()
