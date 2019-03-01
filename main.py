from lib import pygame_window
from lib.classes import Message, Editor, Text
from lib.addons import tab_num

#print(asksaveasfilename().help())

class main(pygame_window.main):
    def __init__(self):
        pygame_window.main.__init__(self, 800, 500, "TREXT")
        self.message = Message(self.display, self.width, "Courier New")


        self.edit = Editor(self.display, self.width, 'config.txt')
        self.background_colour = self.edit.background_colour
        self.run_window = Text(self.display, self.edit.font)

    def update(self):
        #print(self.edit.inp.cursor_position)
        self.edit.update(self.events)
        if self.edit.show_runwindow:
            self.run_window.update([400,10,100,100], ['the','thing'])
        


main().run()
