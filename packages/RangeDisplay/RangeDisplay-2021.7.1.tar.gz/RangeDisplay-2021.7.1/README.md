# RangeDisplay 2021.7.1

2D Fractional display widget for Python Tkinter GUI developement.

***Features:***
+ Range Display
+ Dimensions and Colour customisable

# Preview
[![N|Solid](https://github.com/harshvinay752/RangeDisplay/blob/main/plot.PNG?raw=true)](https://github.com/harshvinay752/RangeDisplay)

## Usage

***Importing display***
```
from RangeDisplay.RangeDisplay import RangeDisplay
```

***Creating RangeDisplay widget:***
```
from tkinter.ttk import *
from tkinter import as tk
 
root = tk.Tk()
 
display = RangeDisplay(root, 200, 200)
display.pack()  # or grid or place method could be used

root.mainloop()
```

***Updating display fraction***
``` 
display.update(0.5,0.5,0.75,0.75)
```
***Attributes***

|Attribute|Default value|Acceptable value|
|--|--|--|
|master| N/A | parent like Tk instance, TopLevel, or Frame etc.|
|Width| N/A | width of widget in px |
|Height| N/A | height of widget in px |
|padX | 6 | x padding distributed both sides of widget|
|padY | 6 | y padding distributed both sides of widget|
|radiusO | 20 | percentage rounding the corners of base display|
|radiusI | 20 | percentage rounding the corners of inner display|
|bdSize | 2 | thickness of border of displays and reference lines in px|
|bgColor | "#f3ffed" |color of base display|
|bdColor | "#000000" |color of border and reference lines|
|fgColor | "#2ef245" |color of inner display|
|xsf | 0.5 | x start fraction 0 to 1|
|xef | 0.8 | x end fraction 0 to 1|
|ysf | 0.2 | y start fraction 0 to 1|
|yef | 0.6 | y end fraction 0 to 1|


# Words of Developer

This is the first version of this library. It is one of its kind widget for tkinter. When I was developing a tool for my college project I found that at the time no inbuilt or external tool is available for tkinter allowing range selection. However, range selection is a high demand tool specially for applications dealing with data visualizations. I would appreciate any developer from any community who wants to contribute to this project.

Being a graduation student, I am unable to work over it for long. I will try to release next version having more features as soon as possible.



