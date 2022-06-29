## luxconnector

This is a python wrapper for the Lux Client windows solution.
The package will only work on Windows.

# Installation

To install this package follow the these steps:

## Step 1: Drivers

Make sure you have or had a [CytoSmart application installed](http://download.cytosmart.com/).
Recommend is the cell counter given it do not restart itself after closing.
This is needed to have all the correct drivers installed.
It doesn't matter if the app is uninstalled afterwards.

## Step 2: pip install

```
pip install luxconnector
```

# Usage

## Initialization

Make sure at least one lux is physically connected to your computer via a USB3 port.
The luxconnector is an object that maintains the connection with the Lux.
To create the object use the following code:

```
from luxconnector import LuxConnector
connector = LuxConnector(number_of_devices=2)
```

NOTE: Make sure number_of_devices is at least the number of devices you have connected.
If not the luxconnector will look for the missing devices forever.

## Getting serial numbers

Each physical device has a serial number.
This number is needed to send commands to a specific device.

```
serial_numbers = connector.get_all_serial_numbers()
```

## Getting a single image

When you want a single image taken at this moment use get_image.
This will return the image as a [`pillow image`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
You need to give the serial number of the device you want to target

```
img = connector.get_image(serial_number)
```

or

```
img = connector.get_image(serial_numbers[index])
```

## Changing the focus

This function will change the focus for the luxconnector object.
Every image taken after this function will have the new focus.

The focus is in the range 0 until 1. (0.0 and 1.0 are valid entries)

You need to give the serial number of the device you want to target

```
connector.set_focus(serial_number, 0.5)
img1 = connector.get_image(serial_number) # Image with focus of 0.5
connector.set_focus(serial_number, 0.7)
img2 = connector.get_image(serial_number) # Image with focus of 0.7
img3 = connector.get_image(serial_number) # Image with focus of 0.7
```

## Getting the temperature

This function returns the temperature in celsius of the device.

You need to give the serial number of the device you want to target

```
temperature = connector.get_temperature(serial_number)
```

## Change activate camera (fluorescence)

To use fluorescence you will need change the active camera.
The camera can be set to 3 different values, RED, GREEN, or BRIGHTFIELD.
This will only work if your device is a fl device otherwise only BRIGHTFIELD is available.

```
connector.set_active_camera(serial_number, "RED")
connector.set_active_camera(serial_number, "GREEN")
connector.set_active_camera(serial_number, "BRIGHTFIELD")
```

## Change camera setting

Each camera has its own settings.
Not all settings are available for BRIGHTFIELD.

- exposure: The time in milliseconds the camera is detecting light.
- gain: The multiplication of the camera. (Fluo only)
  If very little light goes into the camera sensor make sure the gain is high.
- brightness: Strength of the led when it is on (Fluo only)
- focus_offset: the difference in focus between brightfield and fluo.
  If focus is set to 0.4 and focus_offset for RED is set to 0.1 RED focus is 0.5 (Fluo only)

```
connector.set_camera_settings(serial_number, "RED", 500, gain=30, brightness=5000)
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
```

## Getting a z-stack

This function will return a list of [`pillow images`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
Each image will be at a different focus level.

This code will create a z-stack of 6 images.
The focuses of these images will be [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

You need to give the serial number of the device you want to target

```
list_of_imgs = connector.get_z_stack(serial_number, num_img = 6, start_focus = 0.5, stop_focus = 1)
```

## Changing zoom modes

There are 2 zoom modes: "IN" and "OUT".
While zoomed in the resolution is higher but the ROI is smaller, zoomed out has a higher ROI but a lower resolution.

Changing this will change it for every image or z-stack taken afterwards.

You need to give the serial number of the device you want to target

```
connector.set_zoom(serial_number, "IN")
img1 = connector.get_image(serial_number) # Image is zoomed in
connector.set_zoom(serial_number, "OUT")
img2 = connector.get_image(serial_number) # Image is zoomed out
```

## Live view

The live view of the Lux is hosted at http://localhost:3333/cytosmartservice/live?serialNumber=##########.
This image can only been seen if the live view is turned on (by default the live view is turned on).

You need to give the serial number of the device you want to target at the place of the #-symbols.

```
connector.set_liveview(serial_number, True) # in the browser you can see the image being updated
connector.set_liveview(serial_number, False) # Led of Lux turns off till you take a picture
```

# Developers

Developers of the luxconnector please look at the [`developers readme`](README_DEV.md)

# Credits

- Tom Nijhof
- Kyap
- Nora
