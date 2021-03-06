###############################################
# Main UI component sizes
###############################################

CELL_COLS = 8
CELL_ROWS = 8

CELL_WIDTH = 50
CELL_HEIGHT = CELL_WIDTH

WINDOW_WIDTH = (CELL_COLS + 1) * CELL_WIDTH

MESSAGE_STRIP_TOP = ((CELL_ROWS + 1) * CELL_HEIGHT)
MESSAGE_RIBBON_WIDTH = WINDOW_WIDTH
MESSAGE_RIBBON_HEIGHT = 50

BUTTON_STRIP_TOP = MESSAGE_STRIP_TOP + MESSAGE_RIBBON_HEIGHT
BUTTONS = 5
BUTTON_WIDTH = WINDOW_WIDTH / BUTTONS
BUTTON_HEIGHT = 50

WINDOW_HEIGHT = BUTTON_STRIP_TOP + BUTTON_HEIGHT

FONT_SIZE = 20

###############################################
# RGB Colors
###############################################

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (140, 140, 140)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

###############################################
# Button Details
###############################################

CLEAR_BUTTON_LABEL = "CLEAR"
EDIT_BUTTON_LABEL = "EDIT"
PLAY_BUTTON_LABEL = "PLAY"
SOLVE_BUTTON_LABEL = "SOLVE"
QUIT_BUTTON_LABEL = "QUIT"

BUTTON_BORDER_SIZE = 2

BUTTON_ENABLED_BORDER_COLOR = WHITE
BUTTON_ENABLED_COLOR = BLACK
BUTTON_ENABLED_LABEL_COLOR = WHITE

BUTTON_DISABLED_BORDER_COLOR = LIGHT_GRAY
BUTTON_DISABLED_COLOR = DARK_GRAY
BUTTON_DISABLED_LABEL_COLOR = LIGHT_GRAY
BUTTON_FONT_SIZE = FONT_SIZE

###############################################
# Label Details
###############################################

LABEL_BORDER_SIZE = 1

LABEL_BORDER_COLOR = BLACK
LABEL_COLOR = WHITE
LABEL_FONT_COLOR = BLACK
LABEL_FONT_SIZE = FONT_SIZE

###############################################
# Number Cells
###############################################

NUMBER_CELL_BORDER_SIZE = 2

NUMBER_CELL_BORDER_COLOR = LIGHT_GRAY
NUMBER_CELL_COLOR = BLACK
NUMBER_CELL_NORMAL_LABEL_COLOR = WHITE
NUMBER_CELL_CORRECT_LABEL_COLOR = GREEN
NUMBER_CELL_INCORRECT_LABEL_COLOR = RED
NUMBER_CELL_FONT_SIZE = FONT_SIZE

###############################################
# Cell States
###############################################

CELL_EMPTY = 0
CELL_HORIZONTAL = 1
CELL_VERTICAL = 2
CELL_TOP_LEFT = 3
CELL_TOP_RIGHT = 4
CELL_BOTTOM_RIGHT = 5
CELL_BOTTOM_LEFT = 6
TOTAL_CELL_STATES = 7

###############################################
# Cell Colors and Sizes
###############################################

CELL_BORDER_SIZE = 2
CELL_BORDER_COLOR = LIGHT_GRAY
CELL_COLOR = WHITE

CELL_TRACK_GOOD_COLOR = GREEN
CELL_TRACK_BAD_COLOR = RED
CELL_TRACK_SIZE = 4

###############################################
# PyGame
###############################################

CLOCK_TICK = 30
