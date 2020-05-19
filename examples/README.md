The *config.json* file allows for configuration of the timer fonts
and colours, as well as the information shown in the bottom
section, the number of segments included, and the position of the
active split. All the keys are necessary - only change the
corresponding values. The keys are intended to be self-explanatory,
but in case they are not there is a list of keys and what they are
used for. Note that all fonts in Python are defined as a list with
2 elements: ["Font name as string",font size as int].

- buttonFont: The font used for the buttons on the bottom
- mainFont: The font used for the segments and general information
- segmentFont: The font used for the segment timer
- timerFont: The font used for main timer
- activeColour: The colour used to indicate which split is the
  current one
- buttonBgColour: The colour of the buttons
- buttonTextColour: The colour of the text on the buttons
- endColour: The colour of the last segment, used to differentiate
  the final segment from the rest of them
- mainColour: The colour for the rest of the segments and general
  information
- segmentColour: The colour of the segment timer
- timerColour: The colour of the main timer
- numSplits: The number of segments to be shown
- activeSplit: The position of the active segment (for when the
  segment is not too close to the beginning or end). Must be less
  than or equal to numSplits
- timeSaveShow: A boolean to determine whether the possible time
  save is shown in the general info
- diffShow: A boolean to determine whether the difference between
  the previous segment and the best segment is shown in the general
  info
- bptShow: A boolean to determine whether the best possible time is
  shown in the general info
- sobShow: A boolean to determine whether the sum of bests is shown
  in the general info
- pbShow: A boolean to determine whether the personal best time is
  shown in the general info
