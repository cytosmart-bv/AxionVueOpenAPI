[![Downloads](https://pepy.tech/badge/AxionVueOpenAPI)](https://pepy.tech/project/AxionVueOpenAPI)
[![Downloads](https://pepy.tech/badge/CytoSmartOpenAPI)](https://pepy.tech/project/CytoSmartOpenAPI)
[![Downloads](https://pepy.tech/badge/luxconnector)](https://pepy.tech/project/luxconnector)

# Axion Vue Open API

This is a Python wrapper for the Axion Vue Windows app to use it headless.
The package will only work on Windows 10 and above.

This package was formally known as `luxconnector` or `CytoSmartOpenAPI`

## Warranty

> ⚠️ **Hardware warranty is void by using this open API** ⚠️:
>
> Using the AxionVueOpenAPI means you will have NO hardware warranty (see license).

This is because our devices are made to handle the normal usage ([the GUI app](https://download.axionbio.com/)).
It also includes additionally bought warranty.
Only if your additionally bought warranty implicitly includes the Open API usage you will have warranty.

## Installation

To install this package follow these steps:

### Step 1: Drivers

Make sure you had a [Axion Vue application installed](http://download.axionbio.com/).

Recommended is the cell counter given it does not restart itself after closing.
This is needed to have all the correct drivers installed.
Uninstall the app afterwards.
If the app is on the same machine the Open API might connect with the wrong one.

### Step 2: pip install

```cmd
pip install AxionVueOpenAPI
```

## Initialization

Make sure at least one Axion imaging device is physically connected to your computer via a USB3 port.
The AxionVueOpenAPI is an object that maintains the connection with the device.
To create the object use the following code:

```python
from AxionVueOpenAPI import AxionVueOpenAPI
connector = AxionVueOpenAPI(number_of_devices=2, warranty=False)
```

> ⚠️ You are voiding your warranty by using this package

NOTE: Make sure number_of_devices does not exceed the number of devices you have physically connected.
Otherwise the AxionVueOpenAPI will look for the missing devices forever.

## Getting serial numbers

Each physical device has a serial number.
This number is needed to send commands to a specific device.

```python
serial_numbers = connector.get_all_serial_numbers()
```

## Getting a single image

When you want a single image taken at this moment use get_image.
This will return the image as a [`pillow image`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
You need to give the serial number of the device you want to target.

```python
img = connector.get_image(serial_number)
```

or

```python
img = connector.get_image(serial_numbers[index])
```

## Changing the focus

This function will change the focus for the AxionVueOpenAPI object.
Every image taken after this function will have the new focus.

The focus is in the range 0 until 1. (0.0 and 1.0 are valid entries)

You need to give the serial number of the device you want to target.

```python
connector.set_focus(serial_number, 0.5)
img1 = connector.get_image(serial_number) # Image with focus of 0.5
connector.set_focus(serial_number, 0.7)
img2 = connector.get_image(serial_number) # Image with focus of 0.7
img3 = connector.get_image(serial_number) # Image with focus of 0.7
```

## Auto focus

The device goes over multiple possible focuses to find the best focus.
It will use image analysis to determine how well the image is in focus.

```python
# Fast but goes over a limited range to cover most manufactured cell counting slides
connector.do_autofocus(serial_number, "slide")
# Fastest: goes over the limited range where cells can be in focus on the Axion Exact slide
connector.do_autofocus(serial_number, "CSslide")
# Slow, but goes over the full range of possible focusses: suitable for any vessel that works with the Axion imaging device
connector.do_autofocus(serial_number, "other")
```

## Getting the temperature

This function returns the temperature in Celsius of the device.

You need to give the serial number of the device you want to target.

```python
temperature = connector.get_temperature(serial_number)
```

## Change active camera (fluorescence)

To use fluorescence you will need to change the active camera.
The camera can be set to 3 different values, RED, GREEN, or BRIGHTFIELD.
This will only work if your device is an FL device otherwise only BRIGHTFIELD is available.

```python
connector.set_active_camera(serial_number, "RED")
connector.set_active_camera(serial_number, "GREEN")
connector.set_active_camera(serial_number, "BRIGHTFIELD")
```

## Change camera setting

Each camera has its own settings.
Not all settings are available for BRIGHTFIELD.

- exposure: The time in milliseconds that the camera is detecting light. (Lux and Exact devices only; for Omni devices use flash duration)
- gain: The multiplication of the camera. (Fluo only)
  If very little light goes into the camera sensor make sure the gain is high.
- brightness: Strength of the led when it is on. (Fluo only)
- focus_offset: The difference in focus between brightfield and fluo.
  If focus is set to 0.4 and focus_offset for RED is set to 0.1 RED focus is 0.5 (Fluo only)

```python
connector.set_camera_settings(serial_number, "RED", 500, gain=30, brightness=5000, focus_offset=0.0)
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
```

## Change flash duration (Omni only)

The Omni cannot change the exposure time but can change the time the led is on.
This can be done with set_flash_duration.
It will set the duration between 40 and 250 μs.

```python
connector.set_flash_duration(serial_number, duration=120)
```

If you do NOT have an Omni use set_camera_settings.

## Getting a z-stack

This function will return a list of [`pillow images`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
Each image will be at a different focus level.

This code will create a z-stack of 6 images.
The focuses of these images will be [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

You need to give the serial number of the device you want to target.

```python
list_of_imgs = connector.get_z_stack(serial_number, num_img = 6, start_focus = 0.5, stop_focus = 1)
```

## Change stage (Omni only)

To change the position of the Omni stage (camera, led, arm, ect.) give the new position in mm.

- Position x in mm
- Position y in mm
- Time in seconds it can wait till it arrives (default 60)

```python
connector.move_stage(serial_number, 100, 100, 60)
```

After this the normal process for obtaining and changing cameras applies.

## Get stage position (Omni only)

If you need to know where the stage is, use get_position.
This also works if the Omni moved without a move_stage command (e.g. when it goes to sleep).

```python
print(connector.get_position(serial_number))
```

## Changing zoom modes (Lux only)

There are 2 zoom modes: "IN" and "OUT".
While zoomed in the resolution is higher but the ROI is smaller, zoomed out has a higher ROI but a lower resolution.
Since zooming in comprises digital zoom, the image will not show more sample details.

Changing this setting will change it for every image or z-stack taken afterwards.

You need to give the serial number of the device you want to target.

```python
connector.set_zoom(serial_number, "IN")
img1 = connector.get_image(serial_number) # Image is zoomed in
connector.set_zoom(serial_number, "OUT")
img2 = connector.get_image(serial_number) # Image is zoomed out
```

## Live view

The live view of the device is hosted at http://localhost:3333/cytosmartservice/live?serialNumber=##########.
This image can only been seen if the live view is turned on (by default the live view is turned on).

You need to give the serial number of the device you want to target at the place of the #-symbols.

```python
connector.set_liveview(serial_number, False) # Led of device turns off till you take a picture
connector.set_liveview(serial_number, True) # In the browser you can see the image being updated
connector.open_liveview(serial_number) # Opens liveview in the default browser
```

## Developers

Developers of the AxionVueOpenAPI please look at the [`developers readme`](README_DEV.md)

## Credits

- Tom "RoadRunner" Nijhof
- Nora
- Tessa
- Marc "it is with a c" van Vijven
- Julia "I did not break it, I tested it" van den Beemd
- Count Nicolai Vondracek, Señior sunshine manager
