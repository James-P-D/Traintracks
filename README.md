# Traintracks
Traintrack puzzle game in Python

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/screenshot.gif)

## Details

Traintrack puzzles are one-player games published in some UK newspapers. Here is an example from The Times newspaper Friday June 5 2020:

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/traintracks_times_newspaper_no_1037.jpg)

The objective of the game is to complete the traintrack between start point **A** and end point **B**. Each cell can be assigned a horizontal or vertical piece of track, or a track which goes from two adjacent sides. The track cannot cross itself and the puzzle is only complete when the number of pieces of track in each row and column matches the number at the top and side.

More examples of Traintrack puzzles can be found on the [Puzzle Phil website](https://puzzlephil.com/puzzles/dampfross/en/).

## Algorithm

To solve the puzzle we simply perform a depth-first search starting at the first terminal. At each cell we then calculate the next possible piece that can be connected, and then continue this process until we reach the end terminal cell. If we reach a wall or another piece that we cannot connect to, the algorithm back-tracks and tried other pieces. To make the process slightly more efficient, we do not need to perform an exhaustive search as we can back-track early if find that have already surpassed the number of cells in the current row or column.

## Details

After running the application, we are presented with an `8x8` grid of empty cells. We can then change the value of the numerical cells at the top-most row, and on the right-most column by clicking on them. We can also toggle through the possible values for the track cells by clicking on them. See the example below where we build the puzzle from The Times Newspaper:

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/make_puzzle.gif)

Once we have created the board, the user can press the <kbd>PLAY</kbd> button and manually solve the puzzle:

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/play_puzzle.gif)

If we are unable to manually solve the puzzle, we can click the <kbd>SOLVE</kbd> button to search for a solution:

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/solve_puzzle.gif)

## Setup

For Python we need the following:

[pygame](https://www.pygame.org/news) (Tested with v1.9.6)  
[numpy](https://numpy.org/) (Tested with v1.18.3)  

```
pip install pygame
pip install numpy
```