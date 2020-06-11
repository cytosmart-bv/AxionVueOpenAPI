luxconnector
-----

This is a python wrapper around the Lux Client windows solution.
The package will only work on windows.

# Installation
To install this package follow the these steps:

## Step 1: Divers
Make sure you have or had a [CytoSmart application installed](http://download.cytosmart.com/). 
This is needed to have all the correct drivers installed.
It doesn't matter if the app is uninstalled afterwards

## Step 2: pip install
```
pip install luxconnector
```

# Usage

Make sure the lux is physical connected to your computer via an USB3 port.
The luxconnector is an object that maintains the connection with the Lux.
To create the object use the following code:

```
from luxconnector import LuxConnector
connector = LuxConnector()
```

## Getting a single image
When you want a single image taken at this moment use get_image.
This will return the image as a [`numpy array`](https://numpy.org/doc/1.18/reference/generated/numpy.array.html).

```
img = connector.get_image()
```

## Changing the focus
This function will change the focus for the luxconenctor object.
Every image taken after this function will have the new focus.

The focus is in the range 0 till 1. (0.0 and 1.0 are valid entries)

```
connector.set_focus(0.5)
img1 = connector.get_image() # Image with focus of 0.5
connector.set_focus(0.7)
img2 = connector.get_image() # Image with focus of 0.7
img3 = connector.get_image() # Image with focus of 0.7
```

## Getting a z-stack
This function will return list of [`numpy arrays`](https://numpy.org/doc/1.18/reference/generated/numpy.array.html).
Each image will be at a different focus.

This code will create a z-stack of 6 images.
The focusses of these images will be [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
```
list_of_imgs = connector.get_z_stack(num_img = 6, start_focus = 0.5, stop_focus = 1)
```

## Changing zoom modes
There are 2 zoom modes: "IN" and "OUT".
Well zoomed in the resolution is higher but the ROI is smaller, zoomed out has an higher ROI but lower resolution.

Changing it will change it for every image or z-stack taken afterwards.

```
connector.set_zoom("IN")
img1 = connector.get_image() # Image is zoomed in
connector.set_zoom("OUT")
img2 = connector.get_image() # Image is zoomed out
```

## Live view
The live view of the lux is hosted at http://localhost:3333/luxservice/live.
This image can only been seen if the live view is turned on (by default the live view is turned on).

```
connector.set_liveview(True) # in the browser you can see the image being updated
connector.set_liveview(False) # Led of Lux turns off till you take a picture
```

# Credits

- Tom Nijhof
