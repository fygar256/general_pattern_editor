GENERAL PATTERN EDITOR gp.py

Free-size general binary screen pattern editor.

```
0 0 1 1 1 1 0 0 0
0 1 1 0 0 1 1 0 0
1 1 0 0 0 0 1 1 0
1 1 0 0 0 0 1 1 0
1 1 1 1 1 1 1 1 0
1 1 0 0 0 0 1 1 0
1 1 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0
```

Edit and generate a text file of a two-dimensional list of 0 and 1.

Give execurion right as:

```
chmod +x gp.py
```

```
Usage: ./gp.py file
```

You can load the 2 dimentional list from file with numpy

```
import numpy as np
F = np.loadtxt(a)
```

You can save it with:

```
np.savetxt(a, F, “%d”)
```

Editor commands

```
'w' save and quit.
'z' set the number of elements for the current screen width and height.
'c' clear the current screen.
'q' quit.
```

On/Off after mouse click on a cell of the screen. The first screen has 8x8 elements.

After entering a command that takes arguments, a message will appear in the window you launched, but it will not be focused, so click on it to focus it.
