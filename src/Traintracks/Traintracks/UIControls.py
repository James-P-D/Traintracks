import pygame
from Constants import *
import datetime

###############################################
# NumberCell()
###############################################

class NumberCell():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __value = 0
    __enabled = True
    __correct = False

    def __init__(self, x, y, width, height, value = 0):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.__value = value

    def draw(self, screen):        
        pygame.draw.rect(screen, NUMBER_CELL_BORDER_COLOR, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, NUMBER_CELL_COLOR, (self.__x + NUMBER_CELL_BORDER_SIZE, self.__y + NUMBER_CELL_BORDER_SIZE, self.__width - (NUMBER_CELL_BORDER_SIZE * 2), self.__height - (NUMBER_CELL_BORDER_SIZE * 2)), 0)

        if (self.__value != -1):
            label_font = pygame.font.SysFont('courier', NUMBER_CELL_FONT_SIZE, bold = True)
            label_text = label_font.render(str(self.__value), 1, self.__get_font_color())
            label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
            label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
            screen.blit(label_text, (int(label_x), int(label_y)))

    def __get_font_color(self):
        if self.__enabled:
           return NUMBER_CELL_NORMAL_LABEL_COLOR
        elif self.__correct:
            return NUMBER_CELL_CORRECT_LABEL_COLOR
        else:
            return NUMBER_CELL_INCORRECT_LABEL_COLOR

    def is_over(self, mouse_x, mouse_y):
        return ((mouse_x >= self.__x) and (mouse_x < (self.__x + self.__width)) and (mouse_y >= self.__y) and (mouse_y < (self.__y + self.__height)))
        
    def inc_value(self, cap):
        self.__value = (self.__value + 1) % cap

    def get_value(self):
        return self.__value

    def is_enabled(self):
        return self.__enabled

    def enable(self):
        self.__enabled = True
    
    def disable(self):
        self.__enabled = False

    def set_correct(self):
        self.__correct = True

    def set_incorrect(self):
        self.__correct = False


###############################################
# Cell()
###############################################

class Cell():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __state = CELL_EMPTY
    __enabled = True

    def __init__(self, x, y, width, height, state = CELL_EMPTY):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.__state = state

    def draw(self, screen, is_correct):     
        
        def draw_left_line(cell_track_color):
            x1 = self.__x + CELL_BORDER_SIZE
            y1 = self.__y + (CELL_HEIGHT / 2)
            x2 = x1 + ((CELL_WIDTH - (2 * CELL_BORDER_SIZE)) / 2)
            y2 = y1
            pygame.draw.line(screen, cell_track_color, (x1, y1), (x2, y2), CELL_TRACK_SIZE)

        def draw_right_line(cell_track_color):
            x1 = self.__x + CELL_BORDER_SIZE + ((CELL_WIDTH - (2 * CELL_BORDER_SIZE)) / 2)
            y1 = self.__y + (CELL_HEIGHT / 2)
            x2 = x1 + ((CELL_WIDTH - (2 * CELL_BORDER_SIZE)) / 2)
            y2 = self.__y + (CELL_HEIGHT / 2)
            pygame.draw.line(screen, cell_track_color, (x1, y1), (x2, y2), CELL_TRACK_SIZE)

        def draw_top_line(cell_track_color):
            x1 = self.__x + CELL_BORDER_SIZE + ((CELL_WIDTH - (2 * CELL_BORDER_SIZE)) / 2)
            y1 = self.__y + CELL_BORDER_SIZE
            x2 = x1
            y2 = self.__y + (CELL_HEIGHT / 2)
            pygame.draw.line(screen, cell_track_color, (x1, y1), (x2, y2), CELL_TRACK_SIZE)

        def draw_bottom_line(cell_track_color):
            x1 = self.__x + CELL_BORDER_SIZE + ((CELL_WIDTH - (2 * CELL_BORDER_SIZE)) / 2)
            y1 = self.__y + (CELL_HEIGHT / 2)
            x2 = x1
            y2 = y1 + ((CELL_HEIGHT - (2 * CELL_BORDER_SIZE)) / 2)
            pygame.draw.line(screen, cell_track_color, (x1, y1), (x2, y2), CELL_TRACK_SIZE)


        pygame.draw.rect(screen, CELL_BORDER_COLOR, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, CELL_COLOR, (self.__x + CELL_BORDER_SIZE, self.__y + CELL_BORDER_SIZE, self.__width - (CELL_BORDER_SIZE * 2), self.__height - (CELL_BORDER_SIZE * 2)), 0)
        cell_track_color = CELL_TRACK_GOOD_COLOR if is_correct else CELL_TRACK_BAD_COLOR
    
        if (self.__state == CELL_HORIZONTAL):
            draw_left_line(cell_track_color)  
            draw_right_line(cell_track_color)  
        elif (self.__state == CELL_VERTICAL):
            draw_top_line(cell_track_color)
            draw_bottom_line(cell_track_color)
            pass
        elif (self.__state == CELL_TOP_LEFT):
            draw_left_line(cell_track_color)  
            draw_top_line(cell_track_color)
            pass
        elif (self.__state == CELL_TOP_RIGHT):
            draw_top_line(cell_track_color)
            draw_right_line(cell_track_color)  
            pass
        elif (self.__state == CELL_BOTTOM_RIGHT):
            draw_right_line(cell_track_color)  
            draw_bottom_line(cell_track_color)
            pass
        elif (self.__state == CELL_BOTTOM_LEFT):
            draw_bottom_line(cell_track_color)
            draw_left_line(cell_track_color)  
            pass
        
    def inc_state(self):
        self.__state = (self.__state + 1) % TOTAL_CELL_STATES

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state

    def is_enabled(self):
        return self.__enabled

    def enable(self):
        self.__enabled = True
    
    def disable(self):
        self.__enabled = False

###############################################
# Label()
###############################################

class Label():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __label = ""

    def __init__(self, x, y, width, height, label = ""):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.__label = label

    def draw(self, screen):
        pygame.draw.rect(screen, LABEL_BORDER_COLOR, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, LABEL_COLOR, (self.__x + LABEL_BORDER_SIZE, self.__y + LABEL_BORDER_SIZE, self.__width - (LABEL_BORDER_SIZE * 2), self.__height - (BUTTON_BORDER_SIZE * 2)), 0)

        label_font = pygame.font.SysFont('courier', LABEL_FONT_SIZE, bold = True)
        label_text = label_font.render(self.__label, 1, LABEL_FONT_COLOR)
        label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
        label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
        screen.blit(label_text, (int(label_x), int(label_y)))

    def clear(self):
        self.set_label("")
        
    def set_label(self, label):
        self.__label = label + " " + datetime.datetime.now().strftime("%I:%M:%S")

###############################################
# Button()
###############################################

class Button():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __label = ""
    __enabled = True

    def __init__(self, x, y, width, height, label, enabled):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.__label = label
        self.__enabled = enabled

    def draw(self, screen):
        button_border_color = BUTTON_ENABLED_BORDER_COLOR if self.__enabled else BUTTON_DISABLED_BORDER_COLOR
        button_color = BUTTON_ENABLED_COLOR if self.__enabled else BUTTON_DISABLED_COLOR
        button_font_color = BUTTON_ENABLED_LABEL_COLOR if self.__enabled else BUTTON_DISABLED_LABEL_COLOR

        pygame.draw.rect(screen, button_border_color, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, button_color, (self.__x + BUTTON_BORDER_SIZE, self.__y + BUTTON_BORDER_SIZE, self.__width - (BUTTON_BORDER_SIZE * 2), self.__height - (BUTTON_BORDER_SIZE * 2)), 0)

        label_font = pygame.font.SysFont('courier', BUTTON_FONT_SIZE, bold = True)
        label_text = label_font.render(self.__label, 1, button_font_color)
        label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
        label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
        screen.blit(label_text, (int(label_x), int(label_y)))

    def is_over(self, mouse_x, mouse_y):
        return ((mouse_x >= self.__x) and (mouse_x < (self.__x + self.__width)) and (mouse_y >= self.__y) and (mouse_y < (self.__y + self.__height)))
        
    def is_enabled(self):
        return self.__enabled

    def enable(self):
        self.__enabled = True
    
    def disable(self):
        self.__enabled = False