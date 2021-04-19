# splitNames.csv

In the parent directory, there should be a file called
*splitNames.csv*. This file contains all the games, categories, and
split names for each category. 

This file should contain
the name of the game and category to be played in the first two
columns, and the names of all the desired segments starting in the
same column. The first column is for games, and the second for
categories. An example of a row is
```
Super Mario Bros.,Any%,World 1-1,World 1-2,World 4-1,World
4-2,World 8-1,World 8-2,World 8-3,World 8-4
```
The game only needs to be given once, and all the categories should be
in a block on that line and the ones after it. For example, if
there are two categories for *Super Mario Bros.*, the two
categories should be on consecutive lines, and only the first line
should have the name of the game. For example, the second row could
be
```
,World 1 RTA,World 1-1,World 1-2,World 1-3,World 1-4
```

For games that use an in-game timer, it is useful for the timer to
pause automatically between some segments. To identify a segment 
that should pause when it is completed, append `[P]` to the end of
the segment name in *splitNames.csv*. For example, to indicate that
the timer should pause after Chapter 4 in a Celeste speedrun, the
segment for Chapter 4 should be called `Chapter 4 [P]`.

An example is in *splitNames.csv*.
