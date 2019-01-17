import pygame
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename

class Message:
    def __init__(self, display, width, font,font_colour = (0,0,0),
                 bg_colour= (150,150,150), size=36):
        self.display = display
        self.width = width
        self.font = font
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.size = size
        self.font = pygame.font.SysFont(self.font, self.size)

    def update(self, message):
        
        text = self.font.render(message, True, self.font_colour)
        w, h =text.get_size()
        pygame.draw.rect(self.display, self.bg_colour, [self.width - w - 20, 20, w, h])
        self.display.blit(text, (self.width - w - 20, 20))


inp = pygame_textinput.TextInput(font_family=font,
                                 text_color=text_colour,
                                 cursor_color=cursor_colour,
                                 font_size=font_size)
    

      

class main:
    def __init__(self):
        pygame_window.main.__init__(self,display, width, font, bg_colour)
        self.display = display
        self.width = width
        self.font = font
        self.message = Message(self.display, self.width, self.font)
        
        self.background_colour = background_colour
        self.start_position = (10,3)
        self.position = [10,3]
        self.scrole_speed = 20

        self.file_name = None
        self.run_command = 'python ' 


    def update(self, events):
        
        inp.update(events)
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
        
            
