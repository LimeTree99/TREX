import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename

import pygame
from pyhelp import pygame_window, addons
import pyhelp.pygame_textinput

#print(asksaveasfilename().help())





# colour variables
background_colour  = (0,0,0)
text_colour = (255,255,255)
cursor_colour = (255,255,255)

# file variables
defalt_path = os.path.abspath("""C:/Users/verdon/Documents/art""")


# init classes
inp = pyhelp.pygame_textinput.TextInput(font_family="Courier New",
                                        text_color=text_colour,
                                        cursor_color=cursor_colour)
    




class main(pygame_window.main):
    def __init__(self):
        pygame_window.main.__init__(self, 800, 500, "TREXT")
        self.background_colour = background_colour


    def update(self):
        #print(pygame.key.get_mods())
        
        inp.update(self.events)
        inp.render(self.display, 10,10)

        
        if inp.com_codes['ctrl_s']:
            f_name = self.save_file()
            self.save(f_name, inp.get_text())
            inp.com_codes['ctrl_s'] = False

        if inp.com_codes['ctrl_o']:
            lines = self.open_file()
            inp.set_text(lines)
            inp.com_codes['ctrl_o'] = False
            

    def event_handle(self, event):
        pass

    def save_file(self):
        root = tk.Tk()
        root.withdraw()
        root.focus_force()
        file = asksaveasfilename()
        return file
    
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        root.focus_force()
        file = askopenfilename()
        fh = open(file, 'r')
        lines = fh.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip('\n')
        return lines

    def save(self, f_name, lines):
        fh = open(f_name, 'w+')
        for line in lines:
            print(line, file=fh)
        fh.close
            

    

main().run()
