# tkinterflow

This is a project to add the functionality of a 'flow' layout to Python Tkinter graphical user interface module.

Tkinter has the Pack, Grid, and Place geometry managers.

This module adds a Flow option to the geometry managers.

To implement the module, install it first with:
```
pip install tkinterflow
```
then use the following import statements
```
from tkinter import *
from tkinterflow.flowmethods import *
```
Now additional methods can be used.  If you are used to using statements like:
```
button1.pack()
```
#### you can use
```
button1.flow()
```
to add the widgets to a frame.
#### you can use
```
button1.destroy()
```
to remove the button from the frame.

The widgets should flow inside the parent frame like typical flow geometry, like in typical html or just regular text flow like word-wrapping.

You cannot use the flow geometry manager in the root widget, but can use it in any frame below root.

#### So if you only have one root window, pack a frame into the root window, then use flow to add widgets to that frame.  You'll want to make that frame stick to the parent root window so it expands with the root window.

The flow behavior is a subset of the grid geometry manager.

#### Like pack, grid, and place, you should not mix geometry managers.  Likewise with the flow geometry manager.

-If you are flowing into a frame, only use flow, don't try to mix and match geometry managers.
