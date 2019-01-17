import os
import subprocess
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename

import pygame
from pyhelp import pygame_window, addons

import pygame_textinput
from classes import Message


#print(asksaveasfilename().help())





# colour variables
background_colour  = (0,0,0)
text_colour = (255,255,255)
cursor_colour = (255,255,255)

font = "Courier New"
font_size = 24

# file variables
defalt_path = os.path.abspath("""C:/Users/verdon/Documents/art""")


# init classes
inp = pygame_textinput.TextInput(font_family=font,
                                 text_color=text_colour,
                                 cursor_color=cursor_colour,
                                 font_size=font_size)
    

      

class main(pygame_window.main):
    def __init__(self):
        pygame_window.main.__init__(self, 800, 500, "TREXT")
        self.message = Message(self.display, self.width, font)
        
        self.background_colour = background_colour
        self.start_position = (10,3)
        self.position = [10,3]
        self.scrole_speed = 20

        self.file_name = None
        self.run_command = 'python ' 


    def update(self):
        
        inp.update(self.events)
        inp.render(self.display, self.position[0], self.position[1])
        
        
        if inp.com_codes['ctrl_s']:
            self.save(inp.get_text())
            inp.com_codes['ctrl_s'] = False

        elif inp.com_codes['ctrl_shift_s']:
            self.save_as(inp.get_text())
            inp.com_codes['ctrl_shift_s'] = False

        elif inp.com_codes['ctrl_o']:
            lines = self.open_file()
            if lines != None:
                inp.set_text(lines)
            inp.com_codes['ctrl_o'] = False

        elif inp.com_codes['f5']:
            # run
            inp.cursor_position = 10
            
            inp.com_codes['f5'] = False

        elif inp.com_codes['shift_up']:
            self.position[1] += self.scrole_speed
            inp.com_codes['shift_up'] = False

        elif inp.com_codes['shift_down']:
            self.position[1] -= self.scrole_speed
            inp.com_codes['shift_down'] = False

        elif inp.com_codes['shift_right']:
            self.position[0] += self.scrole_speed
            inp.com_codes['shift_right'] = False

        elif inp.com_codes['shift_left']:
            self.position[0] -= self.scrole_speed
            inp.com_codes['shift_left'] = False
            

    def event_handle(self, event):
        pass

    def message(self, message):
        text = font.render("Hello, World", True, (0, 128, 0))
        
        rect = [self.width - window_len, 30, length, height]
        

    def save(self, lines):
        if self.file_name == None:
            self.save_as(lines)
        else:
            fh = open(self.file_name, 'w+')
            for line in lines:
                print(line, file=fh)
            fh.close
        self.message.update('Saved')
    
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        root.focus_force()
        self.file_name = askopenfilename()
        if self.file_name != '':
            fh = open(self.file_name, 'r')
            lines = fh.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip('\n')
        else:
            print('error no file to be opened')
            lines = None
            self.file_name = None
        return lines
    def save_as(self, lines):
        root = tk.Tk()
        root.withdraw()
        root.focus_force()
        self.file_name = asksaveasfilename()
        if self.file_name != '':
            fh = open(self.file_name, 'w+')
            for line in lines:
                print(line, file=fh)
            fh.close
        else:
            print('error no file to be saved')
            self.file_name = None
        
            



main().run()
