import tkinter as tk

window = tk.Tk()

while(True):
    inp = 3
    temp = '#00' + str(hex(int(inp) * 14)) + '00'
    temp = temp[0:3] + temp[5:]
    window['bg'] = temp
    window.attributes('-fullscreen', True)
    window.mainloop()