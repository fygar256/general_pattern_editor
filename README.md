GENERAL PATTERN EDITOR patterneditor.py

Free-size generic binary screen pattern editor.

````
0 0 1 1 1 1 0 0 0
0 1 1 0 0 1 1 0 0
1 1 0 0 0 0 1 1 0
1 1 0 0 0 0 1 1 0
1 1 1 1 1 1 1 1 0
1 1 0 0 0 0 1 1 0
1 1 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0
````

Edit and generate a text file of a two-dimensional list of 0's and 1's.

Load the 2 dimentional list from file with numpy

````.
import numpy as np
F = np.loadtxt(a)
```

You can save it with:

```
np.savetxt(a, F, “%d”)
```
Editor commands

```
With 'l', set the screen width and height to the number of elements in the file, and load the pattern from the file.
        's' to load a pattern from a file.
's' saves the current screen to file.
'z' sets the number of elements for the current screen width and height.
'c' clears the current screen.
With 'q' you are done.
```

On/Off after mouse click on a cell of the screen. The first screen has 8x8 elements.

After entering a command that takes arguments, a message will appear in the window you launched, but it will not be focused, so click on it to focus it. The same is true when you return to the editor.
