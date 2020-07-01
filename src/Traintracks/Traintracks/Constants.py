CELL_COLS = 8
CELL_ROWS = 8

CELL_WIDTH = 50
CELL_HEIGHT = CELL_WIDTH

WINDOW_WIDTH = (CELL_COLS + 2) * CELL_WIDTH

MESSAGE_RIBBON_WIDTH = WINDOW_WIDTH
MESSAGE_RIBBON_HEIGHT = CELL_HEIGHT

BUTTON_STRIP_TOP = ((CELL_ROWS + 2) * CELL_HEIGHT) + MESSAGE_RIBBON_HEIGHT

BUTTONS = 4
BUTTON_WIDTH = WINDOW_WIDTH / BUTTONS
BUTTON_HEIGHT = CELL_HEIGHT

WINDOW_HEIGHT = ((CELL_ROWS + 2) * CELL_HEIGHT) + MESSAGE_RIBBON_HEIGHT + BUTTON_HEIGHT

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

###############################################
# PyGame
###############################################

CLOCK_TICK = 30
SMALL_SLEEP = 0.01
BIG_SLEEP = 0.5