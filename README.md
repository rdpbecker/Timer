# Setup

__Note__: Examples for much of the setup/configuration files can be
found in the `examples` directory, along with a description of each
of the files.

## Category/Segment Names
In the parent directory, create a file called *splitNames.csv*. This 
file stores the list of games and categories, along with the list
of segments for each game/category pair.  More explanation and an 
example are given in the *examples/* directory.

## Configuring the layout

In the `defaults` directory, there is a file called `layout.json`.
This file gives the default layout for the timer. This file
provides a list of objects, where each object defines a component
to be used in the layout. Each object has the form
```
{
    "type" (required): the type of component to add
    "config" (optional): the location of the configuration file for
        this component (if desired). The referenced file has the
        location 'config/<config>.json', so set this appropriately.
}
```

Custom layouts should follow this format, and should be placed in a
directory called `layouts`.

#### Notes about layouts

1. The list of component types are given in
`Components/componentList.json`, and descriptions of each of the
types is given in that directory.

2. If a config location is not given, or if the referenced
configuration file does not exist, the configuration used for the
component is taken from `defaults/<type>.json`. This file defines
all the necessary configuration fields for the given component
type, so look at this when making a component configuration.

3. The defined components are added to the window in order from top to
bottom, so the order of component definitions does matter.

4. Custom layouts can be added to a folder called `layouts`. Before
the window is created, you will be prompted to choose a layout to
use from this directory. `system default` refers to the default layout
defined in the `defaults` directory.

## General configuration notes

As noted before, each component has the option to have custom
configuration, and the components used and their relative positions
are also customizable. However, there is also a global
configuration at `defaults/global.json`. There are only three
attributes defined in this file:

1. `baseDir`: The base directory where all the data is stored
2. `padx`: The (global) horizontal padding on the outside of the
window
3. `showMenu`: A flag which controls whether the control menu is
shown.
3. `hotkeys`: Defines the hotkeys associated with different control
actions. These are validated before being set, and a error will be
shown if an invalid hotkey is defined

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

# Included Programs

__Note__: If the three programs are not installed (see
[Installation](#installation-linux-only) for install instructions) and are just
being run as a Python script, they must be run from this directory
in order to work, as default configuration files are referenced
locally from this directory.

## runTimer.py

Usage: `python3 runTimer.py` (`runTimer` with installation)

This is a segmented timer which keeps track of segments and stores
them in a CSV file when the program is completed (either when the
final segment is completed or when the user terminates the
program).

### How it works

The program starts by prompting the user to choose a game from
those in the first column of *splitNames.csv*. Once the user has
chosen a game, they are prompted to select a category for the game.
When the user selects a category, a GUI pops up which is used for
the rest of the program. By default, there is a menu with a number
of control options, and all the options have an associated hotkey.
Below is a description of each of the options and their default hotkey.

|Function|Description|Hotkey|
|:------:|:---------:|:----:|
|`Start Run`|Starts the timer|`<Space>`|
|`Split`|Ends the current segment and starts the next one|`<Return>`|
|`Reset`|Ends the timer, regardless of whether all segments have been completed|`r`|
|`Skip Split`|Skips the current segment|`s`|
|`Change Compare`|Changes to the next comparison|`<Left>` for counter-clockwise, and `<Right>` for clockwise|
|`Pause`|Toggles whether the timer is paused|`p`|
|`Restart`|After the run has ended, resets the timer|`R`|
|`Finish`|Closes the window, prompting to save if there is unsaved data|`f`|
|`Save`|Saves any unsaved local data|`S`|
|`Choose Run`|Opens a dialog to choose the game and category|`q`|
|`Choose Layout`|Opens a dialog to choose the layout|`l`|

A couple notes about the key bindings:

1. A number of the control options are disabled at certain points
during the run. This is a list of when the control options are
enabled:

|Option|Before Start|During Run|After End|
|:----:|:----------:|:--------:|:-------:|
|`Start Run`|enabled|disabled|disabled|
|`Split`|disabled|enabled|disabled|
|`Reset`|disabled|enabled|disabled|
|`Skip Split`|disabled|enabled|disabled|
|`Change Compare`|enabled|enabled|enabled|
|`Pause`|disabled|enabled|disabled|
|`Restart`|disabled|disabled|enabled|
|`Finish`|enabled|disabled|enabled|
|`Save`|enabled|enabled|enabled|
|`Choose Run`|enabled|disabled|disabled|
|`Choose Layout`|enabled|disabled|disabled|

`Split` and `Skip Split` are also disabled when the timer is
paused.

2. These key bindings are configurable using the `hotkeys`
section of the configuration.

## practice.py

Usage: `python3 practice.py` (`practiceTimer` with installation)

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

## variance.py

Usage: `python3 variance.py` (`timeVariance` with installation)

This simply computes the variance of all the segments to determine
which ones are most and least consistent. The variance is presented
as a percentage of the average length of the corresponding segment,
and the segments are printed in descending order by this percent
variance.

The game and category are chosen in the same way as in the other
two programs, and the base directory is read (as usual) from the
user configuration.

# Installation (Linux-only)

If you are using this timer on a Linux machine, there is a simple
install script to add this program to a `bin` folder for easier
use. To install the program, run `./install` in the home directory,
and choose where to install the program. The three executables
created in this case are `runTimer`, `practiceTimer`, and
`timeVariance`. Note that this won't work with the default
configuration, since the default base directory is a relative path.
Instead, set the base directory in the user config to a static
path.
