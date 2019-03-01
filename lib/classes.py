import pygame
from lib import pygame_textinput
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


class Text:
    def __init__(self, display, font, font_colour=(255,255,255),
                 bg_colour=(255,255,255), size=36):
        self.display = display
        self.font = font
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.size = size
        self.font = pygame.font.SysFont(self.font, self.size)

    def update(self, rect, lines):
        pygame.draw.rect(self.display, self.bg_colour, rect, 1)
        for line in lines:
            text = self.font.render(line, True, self.font_colour)
            self.display.blit(text, (rect[0], ))



class fh_pull:
    def string_colour(string):
        """
        changes a string to a colour list
        :param string: in form '(12,1,255)'
        :return: colour (list)
        """
        string = string[1:-1]
        colour = string.split(',')
        for i in range(len(colour)):
            colour[i] = int(colour[i].strip())
        return colour

    def split_line(file):
        """
        splits a file into a list with the title and what it holds
        :param fh: file open for reading
        :return: lis
        """
        fh = open(file, 'r')
        lis = []
        lines = fh.readlines()
        fh.close()
        for line in lines:
            strip = line.strip()
            if strip != '':
                if strip[0] != '#':
                    chunk = line.split('=')
                    for i in range(len(chunk)):
                        chunk[i] = chunk[i].strip()

                    lis.append(chunk)

        return lis


    def imp_config(file):
        """
        :param fh: file open for reading
        :return: dict of the configs
        """
        dict = {}
        lines = fh_pull.split_line(file)

        for line in lines:
            peram = line[0]
            if line[1][0] == '(' or line[1][0] == '[':
                add = fh_pull.string_colour(line[1])
            elif line[1][0].isdigit():
                add = int(line[1])
            elif line[0][1] == 'true' or line[0][1] == 'True':
                add = True
            elif line[0][1] == 'false' or line[0][1] == 'False':
                add = False
            else:
                add = line[1]

            dict[peram] = add
        return dict
      





class Editor:
    def __init__(self, display, width, settings_file):


        self.display = display
        self.width = width

        
        self.start_position = (10,3)
        self.position = [10,3]
        self.scrole_speed = 20
        self.show_runwindow = False

        self.run_command = 'python '

        # all settings imported in the settings dict
        self.font = None
        self.background_colour = None
        self.text_colour = None
        self.cursor_colour = None
        self.font_size = None
        self.tab_size = None
        self.auto_tab = None

        self.load_settings(settings_file)

        self.message = Message(self.display, self.width, self.font)

        self.inp = pygame_textinput.TextInput(font_family=self.font,
                                              text_color=self.text_colour,
                                              cursor_color=self.cursor_colour,
                                              font_size=self.font_size,
                                              tab_size=self.tab_size,
                                              auto_tab=self.auto_tab)


    def load_settings(self, file):
        dic = fh_pull.imp_config(file)
        self.background_colour = dic['background_colour']
        self.font = dic['font']
        self.text_colour = dic['text_colour']
        self.cursor_colour = dic['cursor_colour']
        self.font_size = dic['font_size']
        self.tab_size = dic['tab_size']
        self.auto_tab = dic['auto_tab']


    def update(self, events):
        
        self.inp.update(events)
        self.inp.render(self.display, self.position[0], self.position[1])
        
        
        if self.inp.com_codes['ctrl_s']:

            self.save(self.inp.get_text())
            self.inp.com_codes['ctrl_s'] = False

        elif self.inp.com_codes['ctrl_shift_s']:
            self.save_as(self.inp.get_text())
            self.inp.com_codes['ctrl_shift_s'] = False

        elif self.inp.com_codes['ctrl_o']:
            lines = self.open_file()
            if lines != None:
                self.inp.set_text(lines)
            self.inp.com_codes['ctrl_o'] = False

        elif self.inp.com_codes['f5']:
            #self.show_runwindow = True
            # run
            print('test')
            self.inp.com_codes['f5'] = False

        elif self.inp.com_codes['shift_up']:
            self.position[1] += self.scrole_speed
            self.inp.com_codes['shift_up'] = False

        elif self.inp.com_codes['shift_down']:
            self.position[1] -= self.scrole_speed
            self.inp.com_codes['shift_down'] = False

        elif self.inp.com_codes['shift_right']:
            self.position[0] += self.scrole_speed
            self.inp.com_codes['shift_right'] = False

        elif self.inp.com_codes['shift_left']:
            self.position[0] -= self.scrole_speed
            self.inp.com_codes['shift_left'] = False

        elif self.inp.com_codes['alt_d']:
            #shows and hides the run window
            if self.show_runwindow:
                self.show_runwindow = False
            else:
                self.show_runwindow = True
            self.inp.com_codes['alt_d'] = False

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
        
            
