

try:
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk


def select():
    print var.get()


root = tk.Tk()
root.geometry("%dx%d+%d+%d" % (430, 80, 200, 150))
root.title("Select your image depth")
var = tk.StringVar(root)
# initial value
var.set('Select your depth')
choices = ['1', '2', '3', '4']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
#COMMAND SELECT!
button = tk.Button(root, text="OK", command=select)
button.pack(side='left', padx=20, pady=10)


root.mainloop()