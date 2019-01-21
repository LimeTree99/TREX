import os
import subprocess
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename

import pygame
from lib import pygame_window, addons

from lib import pygame_textinput
from lib.classes import Message, Editor

#print(asksaveasfilename().help())

# variables will be imported from a file in the future
settings = {'font': "Courier New", 'font_size': 24, 'background_colour': (0,0,0),
            'text_colour': (255,255,255), 'cursor_colour': (255,255,255)}

# file variables
defalt_path = os.path.abspath("""C:/Users/verdon/Documents/art""")

# init classes

class main(pygame_window.main):
    def __init__(self):
        pygame_window.main.__init__(self, 800, 500, "TREXT")
        self.message = Message(self.display, self.width, "Courier New")

        self.edit = Editor(self.display, self.width, settings)
        self.background_colour = self.edit.background_colour

    def update(self):
        self.edit.update(self.events)
        


main().run()
