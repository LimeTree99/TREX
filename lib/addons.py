import pygame


def pointcheck(rect, point):
    'checks if the point is in the rect'
    if (rect[0] < point[0] and rect[0] + rect[2] > point[0] and
        rect[1] < point[1] and rect[1] + rect[3] > point[1]):
        return True

def circle_pointcheck(circle_point, radious, point):
    x = circle_point[0] - point[0]
    y = circle_point[1] - point[1]

    dis = (x ** 2 + y ** 2) ** 0.5
    if dis < radious:
        return True


def rect_collide(rect1, rect2):
    'checks all the rects in self.collide against inputed rect.'
    if (pointcheck(rect2, (rect1[0], rect1[1])) or
        pointcheck(rect2, (rect1[0] + rect1[2], rect1[1] + rect1[3])) or
        pointcheck(rect2, (rect1[0] + rect1[2], rect1[1])) or
        pointcheck(rect2, (rect1[0], rect1[1] + rect1[3]))):
        return True
    return False

class collide:
    def __init__(self):
        self.list = []
        self.collide = False

    def add(self, rect):
        self.list.append(rect)

    def _pointcheck(self, rect, point):
        'checks if the point is in the rect'
        if (rect[0] < point[0] and rect[0] + rect[2] > point[0] and
                rect[1] < point[1] and rect[1] + rect[3] > point[1]):
            return True

    def check_all(self):
        'checks all the rects in self.collide against each other.'
        pass

    def check_against(self, rect):
        'checks all the rects in self.collide against inputed rect.'
        for item in self.list:
            if (self._pointcheck(item, (rect[0], rect[1])) or
                    self._pointcheck(item, (rect[0] + rect[2], rect[1] + rect[3])) or
                    self._pointcheck(item, (rect[0] + rect[2], rect[1])) or
                    self._pointcheck(item, (rect[0], rect[1] + rect[3]))):

                self.collide = True
                return
            else:
                self.collide = False

class forever_timer:
    def __init__(self):
        self.first_ex = 0
        self.used = False
        
    def timer(self, interval):
        time = pygame.time.get_ticks()
        if not self.used:
            self.first_ex = pygame.time.get_ticks()
            self.used = True
            return False
        elif time - self.first_ex >= interval:
            return True
        return False
    
    def reset(self):
        self.used = False

class alarm:
    '''
    returns true every time the 'timer' function is called after the given interval
    or after the "alarm" goes off
    '''
    def __init__(self):
        self.old_time = 1
        self.time_ongoing = 0

    def timer(self, interval):
        time = pygame.time.get_ticks()
        if time - self.old_time >= interval:
            self.old_time = time
            return True
        return False
    
class timer:
    
    def __init__(self):
        self.old_time = 0
        self.time_ongoing = 0
        
        
    def get_time(self):
        time = pygame.time.get_ticks()
        self.time_ongoing = time - self.old_time
        return self.time_ongoing

    def reset(self):
        self.old_time += self.time_ongoing
        self.time_ongoing = 0
        
        
        
            

class Sprite(collide):
    """requiors the use of w, s, d, a on the keyboard"""

    def __init__(self, display, colour, x, y, walls=None):
        collide.__init__(self)
        self.display = display
        self.colour = colour
        self.x = x
        self.y = y
        self.walllist=walls
        self.dx = 5
        self.dy = 5
        self.width = 50
        self.height = 50

    def draw(self, keydict):
        
        pygame.draw.rect(self.display, self.colour,
                         [self.x, self.y, self.width, self.height])

        self.update(keydict)

    def update(self, keydict):

        x_buffer = self.x
        y_buffer = self.y

        if keydict['w'] == True:
            y_buffer -= self.dy

        if keydict['s'] == True:
            y_buffer += self.dy
        if keydict['a'] == True:
            x_buffer -= self.dx
        if keydict['d'] == True:
            x_buffer += self.dx


        x_walls = collide.check_against(self, [self.x, y_buffer, self.width, self.height])
        y_walls = collide.check_against(self, [x_buffer, self.y, self.width, self.height])

        if not x_walls:
            self.y = y_buffer
            
        if not y_walls:
            self.x = x_buffer
            




















