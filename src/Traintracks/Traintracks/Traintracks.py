import pygame # Tested with pygame v1.9.6
import numpy as np
from Constants import *
from UIControls import *

###############################################
# Globals
###############################################

grid = np.ndarray((CELL_COLS, CELL_ROWS), np.int8)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clear_button = Button((BUTTON_WIDTH * 0), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, CLEAR_BUTTON_LABEL, True)
play_button = Button((BUTTON_WIDTH * 1), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, PLAY_BUTTON_LABEL, False)
solve_button = Button((BUTTON_WIDTH * 2), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, SOLVE_BUTTON_LABEL, False)
quit_button = Button((BUTTON_WIDTH * 3), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, QUIT_BUTTON_LABEL, True)

###############################################
# game_loop()
###############################################

def game_loop():
    game_exit = False
    clock = pygame.time.Clock()
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True;
        #draw_grid()
        #pygame.display.update()
        clock.tick(CLOCK_TICK)
    pygame.quit()


###############################################
# initialise()
###############################################
def initialise():
    # Set all cells to EMPTY by default
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):
            grid[col, row] = CELL_EMPTY            

###############################################
# initialise()
###############################################
def create_ui():
    screen.fill(BLACK)

    clear_button.draw(screen)
    play_button.draw(screen)
    solve_button.draw(screen)
    quit_button.draw(screen)
    
    #draw_grid()

###############################################
# main()
###############################################

def main():
    pygame.init()
    
    initialise()
    create_ui()

    game_loop()

###############################################
# Startup
###############################################

if __name__ == "__main__":
    main()
