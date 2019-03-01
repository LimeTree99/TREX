"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""

import os.path

import pygame
import pygame.locals as pl

from lib.addons import tab_num

pygame.font.init()


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=35,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            tab_size=4,
            auto_tab=False):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when helpd
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.tab_size = tab_size
        self.input_string = initial_string  # Inputted text
        self.lines = [self.input_string]    # the list where all the lines are stored
        self.line_pointer = 0               # points the the line that the curser is on
        self.auto_tab = auto_tab            # automatic python tab formatting

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # dict for all the keycodes that could be usefull for commands
        self.com_codes = {'ctrl_s':False, 'ctrl_o':False, 'ctrl_shift_s':False,
                          'shift_down':False,'shift_up':False,'shift_left':False,
                          'shift_right':False,'ctrl_down':False,'ctrl_up':False,'ctrl_left':False,
                          'ctrl_right':False,'f5':False, 'alt_f4':False, 'alt_d':False}

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    if self.cursor_position == 0 and self.line_pointer > 0:
                        self.cursor_position = len(self.lines[self.line_pointer - 1])
                        self.lines[self.line_pointer - 1] = self.lines[self.line_pointer - 1] + self.lines[self.line_pointer]
                        self.lines.pop(self.line_pointer)
                        self.line_pointer -= 1
                        self.input_string = self.lines[self.line_pointer]
                    elif self.input_string[:self.cursor_position].strip() == '' and (self.cursor_position) % 4 == 0 and self.cursor_position > 0 and self.auto_tab:
                        self.input_string = self.input_string[self.tab_size:]
                        self.cursor_position -= self.tab_size
                    elif self.cursor_position > len(self.input_string):
                        self.input_string = self.input_string[:-1]
                        self.cursor_position = len(self.input_string)
                    else:
                        self.input_string = (
                            self.input_string[:max(self.cursor_position - 1, 0)]
                            + self.input_string[self.cursor_position:]
                        )
                        # Subtract one from cursor_pos, but do not go below zero:
                        self.cursor_position = max(self.cursor_position - 1, 0)


                # for key codes
                elif (event.key == pl.K_s and
                      (pygame.key.get_mods() & pygame.KMOD_RCTRL or
                       pygame.key.get_mods() & pygame.KMOD_LCTRL)):
                    if (pygame.key.get_mods() & pygame.KMOD_RSHIFT or
                        pygame.key.get_mods() & pygame.KMOD_LSHIFT):
                        self.com_codes['ctrl_shift_s'] = True
                    else:
                        self.com_codes['ctrl_s'] = True

                elif (event.key == pl.K_UP and 
                      (pygame.key.get_mods() & pygame.KMOD_RSHIFT or
                      pygame.key.get_mods() & pygame.KMOD_LSHIFT)):

                    self.com_codes['shift_up'] = True

                elif event.key == pl.K_DOWN and \
                      (pygame.key.get_mods() & pygame.KMOD_RSHIFT or
                      pygame.key.get_mods() & pygame.KMOD_LSHIFT):
                    
                    self.com_codes['shift_down'] = True

                elif event.key == pl.K_RIGHT and \
                      (pygame.key.get_mods() & pygame.KMOD_RSHIFT or
                      pygame.key.get_mods() & pygame.KMOD_LSHIFT):
                    
                    self.com_codes['shift_right'] = True

                elif event.key == pl.K_LEFT and \
                      (pygame.key.get_mods() & pygame.KMOD_RSHIFT or
                      pygame.key.get_mods() & pygame.KMOD_LSHIFT):
                    
                    self.com_codes['shift_left'] = True
                    

                elif (event.key == pl.K_o and
                      (pygame.key.get_mods() & pygame.KMOD_RCTRL or
                      pygame.key.get_mods() & pygame.KMOD_LCTRL)):
                        self.com_codes['ctrl_o'] = True

                elif event.key == pl.K_F5:
                        self.com_codes['f5'] = True

                elif (event.key == pl.K_F4 and
                      pygame.key.get_mods() & pygame.KMOD_ALT):

                    self.com_codes['alt_f4'] = True

                elif (event.key == pl.K_d and
                      pygame.key.get_mods() & pygame.KMOD_ALT):

                    self.com_codes['alt_d'] = True
                
                        
                elif event.key == pl.K_DELETE:
                    if self.cursor_position > len(self.input_string):
                        self.cursor_position = len(self.input_string)
                    if (self.cursor_position == len(self.input_string) and
                        (self.line_pointer != len(self.lines) - 1)):
                        
                        self.input_string = self.lines[self.line_pointer] + self.lines[self.line_pointer + 1]
                        self.lines[self.line_pointer] = self.input_string
                        self.lines.pop(self.line_pointer + 1)
                    else:
                        
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + self.input_string[self.cursor_position + 1:]
                        )

                elif event.key == pl.K_RETURN:
                    self.lines.insert(self.line_pointer +1, self.input_string[self.cursor_position:])
                    self.lines[self.line_pointer] = self.lines[self.line_pointer][:self.cursor_position]

                    tabs = tab_num(self.lines, self.tab_size, self.line_pointer) * self.tab_size

                    self.cursor_position = tabs
                    self.line_pointer += 1

                    self.input_string = (tabs * ' ') + self.lines[self.line_pointer]

                elif event.key == pl.K_RIGHT:
                    if self.line_pointer != len(self.lines) - 1 or \
                       self.cursor_position != len(self.lines[self.line_pointer]):
                        
                        if self.cursor_position >= len(self.lines[self.line_pointer]):
                            self.line_pointer += 1
                            self.cursor_position = 0
                            self.input_string = self.lines[self.line_pointer]
                        else:
                            self.cursor_position += 1

                elif event.key == pl.K_LEFT:
                    if self.line_pointer != 0 or self.cursor_position != 0:
                        if self.cursor_position == 0:
                            self.line_pointer -= 1
                            self.cursor_position = len(self.lines[self.line_pointer])
                            self.input_string = self.lines[self.line_pointer]
                        elif self.cursor_position > len(self.input_string):
                            self.cursor_position = len(self.input_string) - 1
                        else:
                            self.cursor_position -= 1

                elif event.key == pl.K_UP:
                    if self.line_pointer > 0:
                        self.line_pointer -= 1


                    self.input_string = self.lines[self.line_pointer]

                elif event.key == pl.K_DOWN:
                    if self.line_pointer < len(self.lines) - 1:
                        self.line_pointer += 1
                        self.input_string = self.lines[self.line_pointer]
                    elif self.line_pointer == len(self.lines) - 1:

                        self.cursor_position = len(self.input_string)
                        


                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif event.key == pl.K_TAB:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + " " * self.tab_size
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += self.tab_size

               

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]


        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # update the lines
        self.lines[self.line_pointer] = self.input_string
        
        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible
        

        self.clock.tick()
        return False
    
    def render(self,display, x, y):
        for num, i in enumerate(self.lines):
            surface = self.font_object.render(i, self.antialias, self.text_color)
            
            
            if self.cursor_visible and num == self.line_pointer:
                cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
                # Without this, the cursor is invisible when self.cursor_position > 0:
                if len(self.input_string) > 0 and self.cursor_position > 0:
                    cursor_y_pos -= self.cursor_surface.get_width()
                surface.blit(self.cursor_surface, (cursor_y_pos, 0))
            
            display.blit(surface, (x, y))
            height = surface.get_height()
            y += height
            

            
        
    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.lines

    def set_text(self, lines):
        self.lines = lines
        self.line_pointer = 0
        self.cursor_position = 0
        self.input_string = lines[self.line_pointer]
        

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def set_font_size(self, size):
        self.font_size = size
        
    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0
