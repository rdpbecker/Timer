# Setup

In the parent directory, create a file called *splitNames.csv*. 
More explanation and an example are given in the *examples/* 
directory.

The timer is also configurable now! There is an example of a config
file in the *examples/* directory. The real config file should be
in *config.json*, and the program will not run without it. More 
information is in that directory.

# runTimer.py

Usage: python3 runTimer.py

This is a segmented timer which keeps track of segments and stores
them in a CSV file when the program is completed (either when the
final segment is completed or when the user terminates the
program).

## How it works

The program starts by prompting the user to choose a game from
those in the first column of *splitNames.csv*. Once the user has
chosen a game, they are prompted to select a category for the game.
When the user selects a category, a GUI pops up which is used for
the rest of the program. There are six buttons, and most of them
also have key bindings.
1. `Start Run` has the key binding <Space>
2. `Split` has the key binding <Return>
3. `Reset` has the key binding `r`
4. `Skip Split` has the key binding `s`
5. `Change Compare` currently has no key binding
6. `Pause` has the key binding `p`

Each button calls a function to progress through the segments:
1. `Start Run` starts the timer by initializing the start time.
2. `Split` ends the current segment and moves to the next one. The
GUI is also shifted at the end of the segment. **Note**: Don't end
a segment before the timer is initialized, or at the very least
re-initialize the timer if you do. If you end a segment without
initializing the start time, the start time is 0 and the time at
the segment will say it has taken thousands of hours.
3. `Reset` ends the program and timer, and writes the completed
segments as if all the segments have been completed with blank
times for the uncompleted segments.
4. `Skip Split` skips the current segment. The segment timer for
the next timer starts at the time you press this button.
5. `Change Compare` rotates through the possible comparisons. These
are `Personal Best`, `Sum of Bests`, `Average`, and `Last Run`.
6. `Pause` pauses the timer.

# practice.py

Usage: `python3 practice.py`

`practice.py` allows you to practice (and improve bests for)
individual segments. This is run in the same way as `runTimer.py`,
and has mostly the same buttons and key bindings. To choose the
segment, the game and category are chosen in the same way as in
`runTimer.py`, and once the category is chosen the list of segments
is given from which one should be chosen. Hitting `Finish`
will close the window and write the results to the `.csv` file for
that run. Only the best time for the practiced segment will be
written - the sum of best times will be updated with the next run
of `runTimer.py`.

# variance.py

Usage: `python3 variance.py`

This simply computes the variance of all the segments to determine
which ones are most and least consistent. The variance is presented
as a percentage of the average length of the corresponding segment,
and the segments are printed in descending order by this percent
variance.

The game and category are chosen in the same way as in the other
two programs.
