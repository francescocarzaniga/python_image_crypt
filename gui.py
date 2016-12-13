#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFileDialog
import base64

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


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
        self.master.title("G6 - Embedding Secret Messages Into Image Files")

        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button1 = Button(self, text="Hide a message", command=self.embed, width=10)
        self.button1.grid(row=1,column=0)
        self.button2 = Button(self, text="Extract a message", command=self.extract)
        self.button2.grid(row=1,column=1)
        self.button3 = Button(self, text="Show an image", command=self.show)
        self.button3.grid(row=1,column=2)
        self.button4 = Button(self, text="Hide an Image", command=self.embedImage, width=15)
        self.button4.grid(row=1,column=3)
        self.button5 = Button(self, text="Find an Image", command=self.extractImage, width=15)
        self.button5.grid(row=1,column=4)

        self.text1 = Text(self)
        self.text1.insert(END, "Hide your message here!")
        self.text1.grid(row=2,column=0, columnspan=5)

    def embed(self):      
        filename = tkFileDialog.askopenfilename()
        if filename == "":
            return
        img = sl.openimage(filename)
        text = self.text1.get(1.0, END + '-1c')
        #TODO: prendere input la textarea
        Button(root, text='Continue', command=lambda: self.buttonTouched2(text, img, root)).grid(row=3, column=1, sticky=W, pady=4)


    def buttonTouched2(self, text, img, root):
        img_out = sl.embed(text, img)
        filenameout = tkFileDialog.asksaveasfilename()
        if filenameout == "":
            return
        sl.saveimage(img_out, filenameout)
        root.destroy()
    
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

    def embedImage (self):
        imageOriginPath = tkFileDialog.askopenfilename(title = "Select your origin Image", message="Select your origin Image" )
        imageTargetPath = tkFileDialog.askopenfilename(title = "Select your target Image", message ="Select your target Image")

        if imageOriginPath == "":
            return
        if imageTargetPath == "":
            return 
        self.setImageOrigin (sl.openimage(imageOriginPath))
        self.setImageTarget(sl.openimage(imageTargetPath))

        root = tk.Tk()
        root.geometry("%dx%d+%d+%d" % (430, 80, 200, 150))
        root.title("Select your image depth")
        var = tk.StringVar(root)
        # initial value
        var.set('Select your depth')
        choices = [1, 2, 3, 4]
        option = tk.OptionMenu(root, var, *choices)
        option.pack(side='left', padx=10, pady=10)
        #COMMAND SELECT!
        button = tk.Button(root, text="OK", command= lambda:self.buttonTouched(var, root))
        button.pack(side='left', padx=20, pady=10)

    def buttonTouched(self, var, root):
        print var.get()
        embedImagePath = tkFileDialog.asksaveasfilename(message = "Save your image!")
        img_out = sl.putImage(self.getImageOrigin(), self.getImageTarget(), int(var.get()))
        sl.saveimage(img_out, embedImagePath)
        root.destroy()

    def extractImage(self):
        imageToExtractPath = tkFileDialog.askopenfilename(message = "Select your image, which you want to extract")

        if imageToExtractPath == "":
            return

        imageToExtract = sl.openimage(imageToExtractPath)
        img_out = sl.findImage(imageToExtract, 4)

        extractedImagePath = tkFileDialog.asksaveasfilename(message = "Where do you want to save your hidden image?")
        sl.saveimage(img_out, extractedImagePath)

    def storagesize(self, image):
        return int(float(2)/3 * (image.size[0] * image.size[1] * 3 // 8 - len(sl.addmagicstring(""))))

    def setImageOrigin (self, imageOrigin):
        self.imageOrigin = imageOrigin

    def getImageOrigin (self):
        return self.imageOrigin

    def setImageTarget (self, imageTarget):
        self.imageTarget = imageTarget

    def getImageTarget (self):
        return self.imageTarget

def main():
    MyFrame().mainloop()

if __name__ == "__main__":
    main()




















