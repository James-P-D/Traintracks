#TODO:
# * is_complete() doesn't work properly! need to actually trace line, not just count!

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
                            top_number_strip[cell_col].inc_value(CELL_ROWS + 1)
                            top_number_strip[cell_col].draw(screen)
                    elif ((cell_col == CELL_COLS) and (0 < cell_row <= CELL_ROWS)):
                        cell_row -= 1
                        if (right_number_strip[cell_row].is_enabled()):
                            right_number_strip[cell_row].inc_value(CELL_COLS + 1)
                            right_number_strip[cell_row].draw(screen)
                    else:
                        cell_col = int(mouse_x / CELL_WIDTH)
                        cell_row = int(mouse_y / CELL_HEIGHT) - 1 # Reduce row by 1 so we don't include the top_number_strip
                        
                        #print(f"({cell_col}, {cell_row})")
                        if ((cell_col >= 0) and (cell_col < CELL_COLS) and (cell_row >= 0) and (cell_row < CELL_ROWS)):
                            if (grid[cell_col, cell_row].is_enabled()):
                                grid[cell_col, cell_row].inc_state();
                                grid[cell_col, cell_row].draw(screen, False);
                                if (edit_mode):
                                    check_board_state()
                                else:                    
                                    check_top_number_strip(cell_col)
                                    check_right_number_strip(cell_row)

                                    #top_numbers = list(map(lambda n: n.get_value(), top_number_strip))
                                    #right_numbers = list(map(lambda n: n.get_value(), right_number_strip))
                                    #grid_numbers = list(map(lambda x: list(map(lambda y: y.get_state(), x)), grid))
                                    #terminals = get_terminals()
                                    #if len(get_terminals()) == 2:
                                    #    if (Main_is_complete(CELL_COLS, CELL_ROWS, top_numbers, right_numbers, terminals[0], terminals[1], grid_numbers)):
                                    #        message_label.set_label("Complete!")
                                    #        message_label.draw(screen)
                                    #    else:
                                    #        message_label.set_label("Incomplete")
                                    #        message_label.draw(screen)

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
        check_top_number_strip(col)
    for row in range(CELL_ROWS):
        right_number_strip[row].enable()    
        check_right_number_strip(row)
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
        check_top_number_strip(col)
    for row in range(CELL_ROWS):
        right_number_strip[row].disable()    
        check_right_number_strip(row)
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):
            if (grid[col, row].get_state() != CELL_EMPTY):
                grid[col, row].disable();
                grid[col, row].draw(screen, False)

    global edit_mode
    edit_mode = False

###############################################
# solve_button_pressed()
###############################################
def solve_button_pressed():
    terminals = get_terminals()
    if len(get_terminals()) != 2:
        return False
        #TODO: Set label?

    top_numbers = list(map(lambda n: n.get_value(), top_number_strip))
    right_numbers = list(map(lambda n: n.get_value(), right_number_strip))
    grid_numbers = list(map(lambda x: list(map(lambda y: y.get_state(), x)), grid))
    terminals = get_terminals()
                                    
    if (Main_is_complete(CELL_COLS, CELL_ROWS, top_numbers, right_numbers, terminals[0], terminals[1])):
        message_label.set_label("Complete!")
        message_label.draw(screen)
    else:
        (success, new_grid) = Main_solve(CELL_COLS, CELL_ROWS, top_numbers, right_numbers, terminals[0], terminals[1])
        if (success):
            message_label.set_label("Complete!")
            message_label.draw(screen)
            for col in range(CELL_COLS):
                for row in range(CELL_ROWS):
                    new_state = new_grid[col][row]
                    grid[col, row].set_state(new_state)
                    grid[col, row].draw(screen, True)
        else:
            message_label.set_label("No solution found!")
            message_label.draw(screen)

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
# col_diff()
###############################################

def col_diff(col):
    total = 0
    for row in range(CELL_ROWS):
        if (grid[col][row].get_state() != CELL_EMPTY):
            total += 1
        
    return (top_number_strip[col].get_value() - total)

###############################################
# row_diff()
###############################################

def row_diff(row):
    total = 0
    for col in range(CELL_COLS):
        if (grid[col][row].get_state() != CELL_EMPTY):
            total += 1
        
    return (right_number_strip[row].get_value() - total)

###############################################
# check_top_number_strip()
###############################################

def check_top_number_strip(col):
    if (edit_mode):
        top_number_strip[col].set_incorrect()
    else:
        if (col_diff(col) == 0):
            top_number_strip[col].set_correct()
        else:
            top_number_strip[col].set_incorrect()
    top_number_strip[col].draw(screen)

###############################################
# check_right_number_strip()
###############################################

def check_right_number_strip(row):
    if (edit_mode):
        right_number_strip[row].set_incorrect()
    else:
        if (row_diff(row) == 0):
            right_number_strip[row].set_correct()
        else:
            right_number_strip[row].set_incorrect()
    right_number_strip[row].draw(screen)
        
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

def set_other_default_game():
    global top_number_strip
    global right_number_strip    
    global grid
    top_number_strip[0] = NumberCell(CELL_WIDTH * 0, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[1] = NumberCell(CELL_WIDTH * 1, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    top_number_strip[2] = NumberCell(CELL_WIDTH * 2, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    top_number_strip[3] = NumberCell(CELL_WIDTH * 3, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[4] = NumberCell(CELL_WIDTH * 4, 0, CELL_WIDTH, CELL_HEIGHT, 3)
    top_number_strip[5] = NumberCell(CELL_WIDTH * 5, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[6] = NumberCell(CELL_WIDTH * 6, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[7] = NumberCell(CELL_WIDTH * 7, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[0] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 0), CELL_WIDTH, CELL_HEIGHT, 0)
    right_number_strip[1] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 1), CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[2] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 2), CELL_WIDTH, CELL_HEIGHT, 5)
    right_number_strip[3] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 3), CELL_WIDTH, CELL_HEIGHT, 1)
    right_number_strip[4] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 4), CELL_WIDTH, CELL_HEIGHT, 4)
    right_number_strip[5] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 5), CELL_WIDTH, CELL_HEIGHT, 1)
    right_number_strip[6] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 6), CELL_WIDTH, CELL_HEIGHT, 0)
    right_number_strip[7] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 7), CELL_WIDTH, CELL_HEIGHT, 0)
    
    grid[0, 2] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    #grid[1, 1] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (1 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_RIGHT)
    grid[2, 1] = Cell(CELL_WIDTH * 2, (CELL_HEIGHT * (1 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_LEFT)
    #grid[2, 2] = Cell(CELL_WIDTH * 2, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_TOP_RIGHT)
    grid[3, 2] = Cell(CELL_WIDTH * 3, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    grid[4, 2] = Cell(CELL_WIDTH * 4, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_LEFT)
    grid[4, 3] = Cell(CELL_WIDTH * 4, (CELL_HEIGHT * (3 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_VERTICAL)
    grid[4, 4] = Cell(CELL_WIDTH * 4, (CELL_HEIGHT * (4 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_TOP_RIGHT)
    grid[5, 4] = Cell(CELL_WIDTH * 5, (CELL_HEIGHT * (4 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    grid[6, 4] = Cell(CELL_WIDTH * 6, (CELL_HEIGHT * (4 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    grid[7, 4] = Cell(CELL_WIDTH * 7, (CELL_HEIGHT * (4 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_LEFT)
    grid[7, 5] = Cell(CELL_WIDTH * 7, (CELL_HEIGHT * (5 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_TOP_RIGHT)
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            if(grid[col, row] == None):
                grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

def set_very_basic_game():
    global top_number_strip
    global right_number_strip    
    global grid
    top_number_strip[0] = NumberCell(CELL_WIDTH * 0, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[1] = NumberCell(CELL_WIDTH * 1, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    top_number_strip[2] = NumberCell(CELL_WIDTH * 2, 0, CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[0] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 0), CELL_WIDTH, CELL_HEIGHT, 3)
    right_number_strip[1] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 1), CELL_WIDTH, CELL_HEIGHT, 2)
    right_number_strip[2] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 2), CELL_WIDTH, CELL_HEIGHT, 2)
    
    grid[0, 0] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    #grid[1, 0] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    #grid[2, 0] = Cell(CELL_WIDTH * 2, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_BOTTOM_LEFT)
    #grid[2, 1] = Cell(CELL_WIDTH * 2, (CELL_HEIGHT * (1 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_TOP_LEFT)
    #grid[1, 1] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (1 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    #grid[1, 2] = Cell(CELL_WIDTH * 1, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    grid[2, 2] = Cell(CELL_WIDTH * 2, (CELL_HEIGHT * (2 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            if(grid[col, row] == None):
                grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

def set_very_basic_game_again():
    global top_number_strip
    global right_number_strip    
    global grid
    top_number_strip[0] = NumberCell(CELL_WIDTH * 0, 0, CELL_WIDTH, CELL_HEIGHT, 1)
    top_number_strip[1] = NumberCell(CELL_WIDTH * 1, 0, CELL_WIDTH, CELL_HEIGHT, 4)
    top_number_strip[2] = NumberCell(CELL_WIDTH * 2, 0, CELL_WIDTH, CELL_HEIGHT, 3)
    top_number_strip[3] = NumberCell(CELL_WIDTH * 3, 0, CELL_WIDTH, CELL_HEIGHT, 3)
    right_number_strip[0] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 0), CELL_WIDTH, CELL_HEIGHT, 4)
    right_number_strip[1] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 1), CELL_WIDTH, CELL_HEIGHT, 3)
    right_number_strip[2] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 2), CELL_WIDTH, CELL_HEIGHT, 1)
    right_number_strip[3] = NumberCell(CELL_WIDTH * CELL_COLS, CELL_HEIGHT + (CELL_HEIGHT * 3), CELL_WIDTH, CELL_HEIGHT, 3)
    
    grid[0, 0] = Cell(CELL_WIDTH * 0, (CELL_HEIGHT * (0 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    grid[3, 3] = Cell(CELL_WIDTH * 3, (CELL_HEIGHT * (3 + 1)), CELL_WIDTH, CELL_HEIGHT, CELL_HORIZONTAL)
    for col in range(CELL_COLS):
        for row in range(CELL_ROWS):            
            if(grid[col, row] == None):
                grid[col, row] = Cell(CELL_WIDTH * col, (CELL_HEIGHT * (row + 1)), CELL_WIDTH, CELL_HEIGHT)

###############################################
# main()
###############################################

def main():
    pygame.init()
    
    initialise()
    #set_default_game()
    #set_other_default_game()
    #set_very_basic_game()
    set_very_basic_game_again()

    draw_ui()

    game_loop()

###############################################
# Startup
###############################################

if __name__ == "__main__":
    main()
