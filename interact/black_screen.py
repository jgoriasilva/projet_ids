#Code to constantly keep the screen dark (unless the code needs to be run)

import tkinter as tk
from tkinter import ttk
import os

#create black screen
while True:
    root = tk.Tk()
    root.title('GUI')
    root.configure(bg = 'black')
    root.attributes("-fullscreen",True)
    
    #if 'command', then run code
    def key_pressed(event):
        root.destroy()
        os.system('python3 security4.py')
        #quit()
        
    root.bind("<Key>",key_pressed)
    root.mainloop()