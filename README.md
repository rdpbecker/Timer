# Setup

## Category/Segment Names
In the parent directory, create a file called *splitNames.csv*. This 
file stores the list of games and categories, along with the list
of segments for each game/category pair.  More explanation and an 
example are given in the *examples/* directory.

## Layout/Appearance Configuration

Parts of the layout and appearance can be configured by the user.

For the appearance, most of the colours and fonts can be
configured, including but not limited to the main text, the timer,
the buttons, and the highlighting on the current segment.

For the layout, the number of segments displayed and the index of
the current segment can be chosen, and the information shown at the
bottom of the window about the comparisons.

Finally, the base directory of the save files can be configured
using the `baseDir` attribute. The default is to save all files in
the parent of this directory.

A list of all configurable attributes can be found in
`defaultConfig.json`.

## Creating the Configuration

There is a default configuration provided at `defaultConfig.json`
in the root directory. This configuration shouldn't be changed
manually, as it will be overwritten whenever it gets changed in the
repository. To override this configuration globally
(i.e. for all game/category pairs), you can use create a file 
called `config.json` in the root directory which overwrites the
desired attributes. To override this configuration for a specific
game/category pair, create a file at
`<baseDir>/<game>/<category>.json` which overrides the desired
attributes. The attributes are overwritten in the following order:

```
defaultConfig.json -> config.json -> <baseDir>/<game>/<category>.json
```

Attributes in files further right overwrite attributes set in
previous files.

## Manual Comparisons

Comparisons can be added manually using a comparisons file. This
file is automatically created the first time the timer is started
with a particular game/category pair at
`<baseDir>/<game>/<category>_comparisons.csv`. New comparisons can
be added to the right side of this file (the first three
comparisons in the file are expected to be in the positions they
are put in when the file is created). 

Each comparison should have two columns. The left column should be
the time for the given segment, and the right column should be the
total time up the end of the given segment. The title (first entry)
of the second column is used as the name of the comparison.

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

|Function|Description|Hotkey|
|:------:|:---------:|:----:|
|`Start Run`|Starts the timer|`<Space>`|
|`Split`|Ends the current segment and starts the next one|`<Return>`|
|`Reset`|Ends the timer and writes the completed segments, regardless
of whether all segments have been completed|`r`|
|`Skip Split`|Skips the current segment|`s`|
|`Change Compare`|Changes to the next comparison|`<Left>` for counter-clockwise, and `<Right>` for clockwise|
|`Pause`|Toggles whether the timer is paused|`p`|

A couple notes about the key bindings:

1. `Start Run` is disabled after the run has started, and `Split`
is disabled before.

2. These key bindings are configurable using the `hotkeys`
section of the configuration.

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
two programs, and the base directory is read (as usual) from the
user configuration.
