#TODO:
#
# * Need to actually check path in is_complete

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

message_label = Label(0, MESSAGE_STRIP_TOP, MESSAGE_RIBBON_WIDTH, MESSAGE_RIBBON_HEIGHT)

clear_button = Button((BUTTON_WIDTH * 0), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, CLEAR_BUTTON_LABEL, True)
edit_button = Button((BUTTON_WIDTH * 1), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, EDIT_BUTTON_LABEL, False)
play_button = Button((BUTTON_WIDTH * 2), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, PLAY_BUTTON_LABEL, False)
solve_button = Button((BUTTON_WIDTH * 3), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, SOLVE_BUTTON_LABEL, False)
quit_button = Button((BUTTON_WIDTH * 4), BUTTON_STRIP_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, QUIT_BUTTON_LABEL, True)

edit_mode = True

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
                        clear_button_pressed()
                elif (edit_button.is_over(mouse_x, mouse_y)):
                    if (edit_button.is_enabled()):
                        edit_button_pressed()
                elif (play_button.is_over(mouse_x, mouse_y)):
                    if (play_button.is_enabled()):
                        play_button_pressed()
                elif (solve_button.is_over(mouse_x, mouse_y)):
                    if (solve_button.is_enabled()):
                        solve_button_pressed()
                elif (quit_button.is_over(mouse_x, mouse_y)):
                    if (quit_button.is_enabled()):
                        game_exit = True
                else:
                    cell_col = int(mouse_x / CELL_WIDTH)
                    cell_row = int(mouse_y / CELL_HEIGHT)
                    
                    if ((cell_row == 0) and (cell_col != CELL_COLS)):
                        if (top_number_strip[cell_col].is_enabled()):
                            top_number_strip[cell_col].inc_value(CELL_ROWS)
                            top_number_strip[cell_col].draw(screen)
                    elif ((cell_col == CELL_COLS) and (0 < cell_row <= CELL_ROWS)):
                            cell_row -= 1
                            if (right_number_strip[cell_row].is_enabled()):
                                right_number_strip[cell_row].inc_value(CELL_ROWS)
                                right_number_strip[cell_row].draw(screen)
                    else:
                        cell_col = int(mouse_x / CELL_WIDTH)
                        cell_row = int(mouse_y / CELL_HEIGHT) - 1 # Reduce row by 1 so we don't include the top_number_strip
                        print(f"({cell_col}, {cell_row})")
                        if ((cell_col >= 0) and (cell_col < CELL_COLS) and (cell_row >= 0) and (cell_row < CELL_ROWS)):
                            if (grid[cell_col, cell_row].is_enabled()):
                                grid[cell_col, cell_row].inc_state();
                                grid[cell_col, cell_row].draw(screen, False);
                                if (edit_mode):
                                    check_board_state()
                                elif (is_complete()):
                                    message_label.set_label("Complete!")
                                    message_label.draw(screen)

                
            elif event.type == pygame.MOUSEBUTTONUP:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()                

        pygame.display.update()
        clock.tick(CLOCK_TICK)
    pygame.quit()

###############################################
# clear_button_pressed()
###############################################
def clear_button_pressed():
    if (edit_mode):
        initialise();
    else:
        for col in range(CELL_COLS):
            for row in range(CELL_ROWS):
                if (grid[col, row].is_enabled()):
                    grid[col, row].set_state(CELL_EMPTY)

    draw_ui();                        

###############################################
# edit_button_pressed()
###############################################
def edit_button_pressed():
    play_button.disable()
    play_button.draw(screen)

    for col in range(CELL_COLS):
        top_number_strip[col].enable()
    for row in range(CELL_ROWS):
        right_number_strip[row].enable()    
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):
            grid[col, row].enable();

    global edit_mode
    edit_mode = True
    
###############################################
# play_button_pressed()
###############################################
def play_button_pressed():
    edit_button.enable()
    edit_button.draw(screen)

    for col in range(CELL_COLS):
        top_number_strip[col].disable()
    for row in range(CELL_ROWS):
        right_number_strip[row].disable()    
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):
            if (grid[col, row].get_state() != CELL_EMPTY):
                grid[col, row].disable();

    global edit_mode
    edit_mode = False

###############################################
# solve_button_pressed()
###############################################
def solve_button_pressed():
    pass

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
# check_board_state()
###############################################

def check_board_state():
    if len(get_terminals()) != 2:
        message_label.set_label("You must specify 2 terminal points")
        message_label.draw(screen)
        play_button.disable()
        play_button.draw(screen)
        solve_button.disable()
        solve_button.draw(screen)    
        return

    play_button.enable()
    play_button.draw(screen)
    solve_button.enable()
    solve_button.draw(screen)
    message_label.set_label("")
    message_label.draw(screen)
        
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

def get_row_count(row):
    row_count = 0
    for col in range(CELL_COLS):
        if (grid[col, row].get_state() != CELL_EMPTY):
            row_count += 1
    return row_count

###############################################
# is_complete()
###############################################
def is_complete():

    def get_next_cell(col, row, visited_grid):

        def check_cells(col1, row1, col2, row2, visited_grid):
            next_cells = []
            if ((col1 >= 0) and (col1 < CELL_COLS) and (row1 >= 0) and (row1 < CELL_ROWS) and not visited_grid[col1, row1]):
                next_cells.append((col1, row1))
            if ((col2 >= 0) and (col2 < CELL_COLS) and (row2 >= 0) and (row2 < CELL_ROWS) and not visited_grid[col2, row1]):
                next_cells.append((col2, row2))
            return next_cells            

        state = grid[col, row].get_state()
        if (state == CELL_EMPTY):
            pass
        elif (state == CELL_HORIZONTAL):
            return check_cells(col + 1, row, col - 1, row, visited_grid)
        elif (state == CELL_VERTICAL):
            return check_cells(col, row - 1, col, row + 1, visited_grid)
        elif (state == CELL_TOP_LEFT):
            return check_cells(col, row - 1, col - 1, row, visited_grid)
        elif (state == CELL_TOP_RIGHT):
            return check_cells(col, row - 1, col + 1, row, visited_grid)
        elif (state == CELL_BOTTOM_RIGHT):
            return check_cells(col, row + 1, col + 1, row, visited_grid)
        elif (state == CELL_BOTTOM_LEFT):
            return check_cells(col, row + 1, col - 1, row, visited_grid)
        return next_cells

    terminals = get_terminals()
    if len(get_terminals()) != 2:
        return False
        
    for col in range(CELL_COLS):
        col_count = get_column_count(col)
        if (col_count != top_number_strip[col].get_value()):
            return False
    
    for row in range(CELL_ROWS):
        row_count = get_row_count(row)
        if (row_count != right_number_strip[row].get_value()):
            return False

    visited_grid = [[False] * CELL_COLS] * CELL_ROWS

    (first_terminal_col, first_terminal_row) = terminals[0]
    (last_terminal_col, last_terminal_row) = terminals[1]
    col = first_terminal_col
    row = first_terminal_row
    while ((col != last_terminal_col) and (row != last_terminal_row)):
        visited_grid[col_row] = True

        current_cell_state = grid[col][row]
        next_cells = get_next_cell(col, row, visited_grid)

        if (len(next_cells) != 1):
            false
        
        (col, row) = next_cells[0]

    return True;

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
    edit_button.draw(screen)
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
    check_board_state()

###############################################
# initialise()
###############################################
def initialise():
    global top_number_strip
    global right_number_strip    
    global grid
        
    for col in range(CELL_COLS):
        top_number_strip[col] = NumberCell(CELL_WIDTH * col, 0, CELL_WIDTH, CELL_HEIGHT, 0)
   
    for row in range(CELL_ROWS):
        right_number_strip[row] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * row), CELL_WIDTH, CELL_HEIGHT, 0)

    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

###############################################
# set_default_game()
###############################################

def set_default_game():
    global top_number_strip
    global right_number_strip    
    global grid

    top_number_strip[0] = NumberCell(CELL_WIDTH * 0, 0, CELL_WIDTH, CELL_HEIGHT, 5)
    top_number_strip[1] = NumberCell(CELL_WIDTH * 1, 0, CELL_WIDTH, CELL_HEIGHT, 7)
    top_number_strip[2] = NumberCell(CELL_WIDTH * 2, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    top_number_strip[3] = NumberCell(CELL_WIDTH * 3, 0, CELL_WIDTH, CELL_HEIGHT, 6)
    top_number_strip[4] = NumberCell(CELL_WIDTH * 4, 0, CELL_WIDTH, CELL_HEIGHT, 3)
    top_number_strip[5] = NumberCell(CELL_WIDTH * 5, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    top_number_strip[6] = NumberCell(CELL_WIDTH * 6, 0, CELL_WIDTH, CELL_HEIGHT, 3)
    top_number_strip[7] = NumberCell(CELL_WIDTH * 7, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[0] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 0), CELL_WIDTH, CELL_HEIGHT, 4)
    right_number_strip[1] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 1), CELL_WIDTH, CELL_HEIGHT, 6)
    right_number_strip[2] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 2), CELL_WIDTH, CELL_HEIGHT, 5)
    right_number_strip[3] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 3), CELL_WIDTH, CELL_HEIGHT, 5)
    right_number_strip[4] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 4), CELL_WIDTH, CELL_HEIGHT, 3)
    right_number_strip[5] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 5), CELL_WIDTH, CELL_HEIGHT, 4)
    right_number_strip[6] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 6), CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[7] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 7), CELL_WIDTH, CELL_HEIGHT, 1)
    grid[0, 0] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_RIGHT)
    grid[1, 0] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_LEFT)
    grid[0, 1] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (1 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_TOP_LEFT)
    grid[0, 5] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (5 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_VERTICAL)
    grid[1, 7] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (7 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_VERTICAL)
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            if(grid[col, row] == None):
                grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

###############################################
# main()
###############################################

def main():
    pygame.init()
    
    #initialise()
    set_default_game()
    draw_ui()

    game_loop()

###############################################
# Startup
###############################################

if __name__ == "__main__":
    main()
