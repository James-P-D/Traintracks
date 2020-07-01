import pygame # Tested with pygame v1.9.6
import numpy as np
from Constants import *
from UIControls import *

###############################################
# Globals
###############################################

grid = np.ndarray((CELL_COLS, CELL_ROWS), np.int8)
top_number_strip = np.ndarray(CELL_COLS + 1, np.int8)
right_number_strip = np.ndarray(CELL_ROWS + 1, np.int8)
top_number_cells = []
right_number_cells = []

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

message_label = Label(0, MESSAGE_STRIP_TOP, MESSAGE_RIBBON_WIDTH, MESSAGE_RIBBON_HEIGHT, "Test")

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                cell_col = int(mouse_x / CELL_WIDTH)
                cell_row = int(mouse_y / CELL_HEIGHT)
                    
                if ((cell_row == 0) and (cell_col != CELL_COLS)):
                    top_number_strip[cell_col] = (top_number_strip[cell_col] + 1) % (CELL_COLS + 1)
                    top_number_cells[cell_col].set_value(top_number_strip[cell_col])
                    top_number_cells[cell_col].draw(screen)

                elif ((cell_col == CELL_COLS) and (0 < cell_row <= CELL_ROWS)):
                    cell_row -= 1
                    right_number_strip[cell_row] =  (right_number_strip[cell_row] + 1) % (CELL_ROWS + 1)
                    right_number_cells[cell_row].set_value(right_number_strip[cell_row])
                    right_number_cells[cell_row].draw(screen)
                else:
                    cell_col = int(mouse_x / CELL_WIDTH) + 1
                    cell_row = int(mouse_y / CELL_HEIGHT) + 1
                
            elif event.type == pygame.MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()                
                if clear_button.is_over(mouse_x, mouse_y):
                    initialise();
                elif play_button.is_over(mouse_x, mouse_y):
                    pass
                elif solve_button.is_over(mouse_x, mouse_y):
                    pass
                elif quit_button.is_over(mouse_x, mouse_y):
                    game_exit = True
            
        #draw_grid()
        pygame.display.update()
        clock.tick(CLOCK_TICK)
    pygame.quit()

###############################################
# initialise()
###############################################
def initialise():
    global top_number_cells
    global right_number_cells

    for col in range(CELL_COLS):
        top_number_strip[col] = 0
        top_number_cells.append(NumberCell(CELL_WIDTH * col, 0, CELL_WIDTH, CELL_HEIGHT))
    
    for row in range(CELL_ROWS):
        right_number_strip[row] = 0
        right_number_cells.append(NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * row), CELL_WIDTH, CELL_HEIGHT))

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
    
    message_label.draw(screen)

    for col in range(CELL_COLS):
        top_number_cells[col].draw(screen)

    for row in range(CELL_ROWS):
        right_number_cells[row].draw(screen)

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
