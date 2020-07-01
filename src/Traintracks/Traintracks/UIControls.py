import pygame
from Constants import *

###############################################
# NumberCell()
###############################################

class NumberCell():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __value = CELL_EMPTY

    def __init__(self, x, y, width, height):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)

    def draw(self, screen):        
        pygame.draw.rect(screen, NUMBER_CELL_BORDER_COLOR, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, NUMBER_CELL_COLOR, (self.__x + BUTTON_BORDER_SIZE, self.__y + BUTTON_BORDER_SIZE, self.__width - (BUTTON_BORDER_SIZE * 2), self.__height - (BUTTON_BORDER_SIZE * 2)), 0)

        if (self.__value != -1):
            label_font = pygame.font.SysFont('courier', 14)
            label_text = label_font.render(str(self.__value), 1, NUMBER_CELL_LABEL_COLOR)
            label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
            label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
            screen.blit(label_text, (int(label_x), int(label_y)))

    def is_over(self, mouse_x, mouse_y):
        return ((mouse_x >= self.__x) and (mouse_x < (self.__x + self.__width)) and (mouse_y >= self.__y) and (mouse_y < (self.__y + self.__height)))
        
    def set_value(self, value):
        self.__value = value;    

###############################################
# Cell()
###############################################

class Cell():
    __x = 0
    __y = 0
    __width = 0
    __height = 0
    __state = CELL_EMPTY
    __fixed = False

    def __init__(self, x, y, width, height, state, fixed):
        self.__x = int(x)
        self.__y = int(y)
        self.__width = int(width)
        self.__height = int(height)
        self.__state = state
        self.__fixed = fixed

    def draw(self, screen):        
        pygame.draw.rect(screen, CELL_BORDER_COLOR, (self.__x, self.__y, self.__width, self.__height), 0)        
        pygame.draw.rect(screen, CELL_COLOR, (self.__x + BUTTON_BORDER_SIZE, self.__y + BUTTON_BORDER_SIZE, self.__width - (BUTTON_BORDER_SIZE * 2), self.__height - (BUTTON_BORDER_SIZE * 2)), 0)

        label_font = pygame.font.SysFont('courier', 14)
        label_text = label_font.render(self.__label, 1, CELL_FONT_COLOR)
        label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
        label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
        screen.blit(label_text, (int(label_x), int(label_y)))

    def is_over(self, mouse_x, mouse_y):
        return ((mouse_x >= self.__x) and (mouse_x < (self.__x + self.__width)) and (mouse_y >= self.__y) and (mouse_y < (self.__y + self.__height)))
        
    def is_fixed(self):
        return self.__fixed

    def get_state(self):
        return self.__state

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

        label_font = pygame.font.SysFont('courier', 14)
        label_text = label_font.render(self.__label, 1, button_font_color)
        label_x = ((self.__width / 2) - (label_text.get_width() / 2) + self.__x)
        label_y = ((self.__height / 2) - (label_text.get_height() / 2) + self.__y)
        screen.blit(label_text, (int(label_x), int(label_y)))

    def is_over(self, mouse_x, mouse_y):
        return ((mouse_x >= self.__x) and (mouse_x < (self.__x + self.__width)) and (mouse_y >= self.__y) and (mouse_y < (self.__y + self.__height)))
        
    def is_enabled(self):
        return self.__enabled
