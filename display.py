import tkinter as tk
import time 

window = tk.Tk()
inp = 0
while(True):
    time.sleep(.5)
    inp += 1
    inp = inp % 18
    print(inp)
    temp = '#00' + str(hex(int(inp) * 14)) + '00'
    temp = temp[0:3] + temp[5:]
    if len(temp) == 6:
        temp = temp[0] + '0' + temp[1:]
        
    window['bg'] = temp
    print(temp)
    window.attributes('-fullscreen', True)
    window.update()
window.mainloop()