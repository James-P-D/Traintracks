#TODO: Need to actually check path

import pygame # Tested with pygame v1.9.6
import numpy as np
from Constants import *
from UIControls import *

###############################################
# Globals
###############################################

top_number_strip = np.ndarray(CELL_COLS, NumberCell)
right_number_strip = np.ndarray(CELL_ROWS, NumberCell)

grid = np.ndarray((CELL_COLS, CELL_ROWS), Cell)

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
                if (clear_button.is_over(mouse_x, mouse_y)):
                    if (clear_button.is_enabled()):
                        initialise();
                        draw_ui();                        
                elif (play_button.is_over(mouse_x, mouse_y)):
                    if (play_button.is_enabled()):
                        pass
                elif (solve_button.is_over(mouse_x, mouse_y)):
                    if (solve_button.is_enabled()):
                        pass
                elif (quit_button.is_over(mouse_x, mouse_y)):
                    if (quit_button.is_enabled()):
                        game_exit = True
                else:
                    cell_col = int(mouse_x / CELL_WIDTH)
                    cell_row = int(mouse_y / CELL_HEIGHT)
                    
                    if ((cell_row == 0) and (cell_col != CELL_COLS)):
                        top_number_strip[cell_col].inc_value(CELL_ROWS)
                        top_number_strip[cell_col].draw(screen)
                    elif ((cell_col == CELL_COLS) and (0 < cell_row <= CELL_ROWS)):
                        cell_row -= 1
                        right_number_strip[cell_row].inc_value(CELL_ROWS)
                        right_number_strip[cell_row].draw(screen)
                    else:
                        cell_col = int(mouse_x / CELL_WIDTH)
                        cell_row = int(mouse_y / CELL_HEIGHT) - 1 # Reduce row by 1 so we don't include the top_number_strip
                        print(f"({cell_col}, {cell_row})")
                        if ((cell_col >= 0) and (cell_col < CELL_COLS) and (cell_row >= 0) and (cell_row < CELL_ROWS)):
                            grid[cell_col, cell_row].inc_state();
                            grid[cell_col, cell_row].draw(screen, False);
                            terminals = get_terminals()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()                
            
        #draw_grid()
        pygame.display.update()
        clock.tick(CLOCK_TICK)
    pygame.quit()

###############################################
# get_terminals()
###############################################
def get_terminals():
    terminals = []
    for col in range(1, CELL_COLS - 1):
        if (grid[col, 0].get_state() in [CELL_VERTICAL, CELL_TOP_LEFT, CELL_TOP_RIGHT]):
            terminals.append((col, 0))
        if (grid[col, CELL_ROWS - 1].get_state() in [CELL_VERTICAL, CELL_BOTTOM_LEFT, CELL_BOTTOM_RIGHT]):
            terminals.append((col, CELL_ROWS - 1))

    for row in range(1, CELL_ROWS - 1):
        if (grid[0, row].get_state() in [CELL_HORIZONTAL, CELL_TOP_LEFT, CELL_BOTTOM_LEFT]):
            terminals.append((0, row))
        if (grid[CELL_COLS - 1, row].get_state() in [CELL_HORIZONTAL, CELL_TOP_RIGHT, CELL_BOTTOM_RIGHT]):
            terminals.append((CELL_COLS - 1, row))
    
    if (grid[0, 0].get_state() not in [CELL_TOP_LEFT, CELL_BOTTOM_RIGHT, CELL_EMPTY]):
        terminals.append((0, 0))

    if (grid[CELL_COLS - 1, 0].get_state() not in [CELL_TOP_RIGHT, CELL_BOTTOM_LEFT, CELL_EMPTY]):
        terminals.append((CELL_COLS - 1, 0))

    if (grid[0, CELL_ROWS - 1].get_state() not in [CELL_BOTTOM_LEFT, CELL_TOP_RIGHT, CELL_EMPTY]):
        terminals.append((0, CELL_ROWS - 1))

    if (grid[CELL_COLS - 1, CELL_ROWS - 1].get_state() not in [CELL_BOTTOM_RIGHT, CELL_TOP_LEFT, CELL_EMPTY]):
        terminals.append((CELL_COLS - 1, CELL_ROWS - 1))

    print(f"terminals = {terminals}")
    return terminals

###############################################
# get_column_count()
###############################################

def get_column_count(col):
    col_count = 0
    for row in range(CELL_ROWS):
        if (grid[col, row].get_state() != CELL_EMPTY):
            col_count += 1
    return col_count

###############################################
# get_row_count()
###############################################

def get_row_count(col):
    row_count = 0
    for col in range(CELL_COLS):
        if (grid[col, row].get_state() != CELL_EMPTY):
            row_count += 1
    return row_count

###############################################
# is_complete()
###############################################
def is_complete():
    terminals = get_terminals()
    if len(get_terminals()) != 2:
        return False

    first_terminal = terminals[0]
    second_terminal = terminals[1]

    for col in range(CELL_COLS):
        col_count = get_column_count(col)
        if (col_count != top_number_strip[col].get_value()):
            return False
    
    for row in range(CELL_ROWS):
        row_count = get_row_count(row)
        if (row_count != right_number_strip[row].get_value()):
            return False

    #TODO: Need to check that path is actually correct here also!

    return Treu;

###############################################
# draw_cell()
###############################################
def draw_cell(col, row, value, is_correct):        
    pygame.draw.rect(screen, CELL_BORDER_COLOR, (col * CELL_WIDTH, (row + 1) * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 0)        
    pygame.draw.rect(screen, CELL_COLOR, (col * CELL_WIDTH, (row + 1) * CELL_HEIGHT, CELL_WIDTH - (CELL_BORDER_SIZE * 2), CELL_HEIGHT - (CELL_BORDER_SIZE * 2)), 0)        
    
    cell_track_color = CELL_TRACK_GOOD_COLOR if is_correct else CELL_TRACK_BAD_COLOR
    
    if (value == CELL_HORIZONTAL):
        draw_left_line(col, row, cell_track_color)
        pass
    elif (value == CELL_VERTICAL):
        pass
    elif (value == CELL_TOP_LEFT):
        pass
    elif (value == CELL_TOP_RIGHT):
        pass
    elif (value == CELL_BOTTOM_RIGHT):
        pass
    elif (value == CELL_BOTTOM_LEFT):
        pass
        

###############################################
# draw_ui()
###############################################
def draw_ui():
    screen.fill(BLACK)

    clear_button.draw(screen)
    play_button.draw(screen)
    solve_button.draw(screen)
    quit_button.draw(screen)
    
    message_label.draw(screen)

    for col in range(CELL_COLS):
        top_number_strip[col].draw(screen)

    for row in range(CELL_ROWS):
        right_number_strip[row].draw(screen)

    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):
            grid[col, row].draw(screen, False);

###############################################
# initialise()
###############################################
def initialise():
    global top_number_strip
    global right_number_strip    
    global grid
        
    for col in range(CELL_COLS):
        top_number_strip[col] = NumberCell(CELL_WIDTH * col, 0, CELL_WIDTH, CELL_HEIGHT)
    
    for row in range(CELL_ROWS):
        right_number_strip[row] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * row), CELL_WIDTH, CELL_HEIGHT)

    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

###############################################
# main()
###############################################

def main():
    pygame.init()
    
    initialise()
    draw_ui()

    game_loop()

###############################################
# Startup
###############################################

if __name__ == "__main__":
    main()
