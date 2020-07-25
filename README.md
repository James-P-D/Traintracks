# Traintracks
Traintrack puzzle game UI in Python

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/screenshot.gif)

## Details

Traintrack puzzles are one-player games published in some UK newspapers. Here is an example from The Times newspaper Friday June 5 2020:

![Screenshot](https://github.com/James-P-D/Traintracks/blob/master/traintracks_times_newspaper_no_1037.jpg)

The objective of the game is to complete the traintrack between start point **A** and end point **B**. Each cell can be assigned a horizontal or vertical piece of track, or a track which goes from two adjacent sides. The track cannot cross itself and the puzzle is only complete when the number of pieces of track in each row and column matches the number at the top and side.

[paper](https://erikdemaine.org/papers/PathPuzzles_JCDCGGG2017/paper.pdf)
[more puzzles](https://puzzlephil.com/puzzles/dampfross/en/)

## Setup

For Python we need the following:

[pygame](https://www.pygame.org/news) (Tested with v1.9.6)  
[numpy](https://numpy.org/) (Tested with v1.18.3)  

```
pip install pygame
pip install numpy
```