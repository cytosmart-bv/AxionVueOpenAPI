[![Downloads](https://pepy.tech/badge/CytoSmartOpenAPI)](https://pepy.tech/project/CytoSmartOpenAPI)
[![Downloads](https://pepy.tech/badge/luxconnector)](https://pepy.tech/project/luxconnector)

# CytoSMART Open API

This is a python wrapper for the CytoSMART windows app to use it headless.
The package will only work on Windows 10 and above.

This package was formally know as `luxconnector`

## Installation

To install this package follow the these steps:

### Step 1: Drivers

Make sure you have or had a [CytoSmart application installed](http://download.cytosmart.com/).
Recommend is the cell counter given it do not restart itself after closing.
This is needed to have all the correct drivers installed.
Uninstall the app afterwards.
If the app is on the same machine the openAPI might connect with the wrong one.

### Step 2: pip install

```cmd
pip install CytoSmartOpenAPI
```

## Initialization

Make sure at least one CytoSMART device is physically connected to your computer via a USB3 port.
The CytoSmartOpenAPI is an object that maintains the connection with the device.
To create the object use the following code:

```python
from CytoSmartOpenAPI import CytoSmartOpenAPI
connector = CytoSmartOpenAPI(number_of_devices=2)
```

NOTE: Make sure number_of_devices is at least the number of devices you have connected.
If not the CytoSmartOpenAPI will look for the missing devices forever.

## Getting serial numbers

Each physical device has a serial number.
This number is needed to send commands to a specific device.

```python
serial_numbers = connector.get_all_serial_numbers()
```

## Getting a single image

When you want a single image taken at this moment use get_image.
This will return the image as a [`pillow image`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
You need to give the serial number of the device you want to target

```python
img = connector.get_image(serial_number)
```

or

```python
img = connector.get_image(serial_numbers[index])
```

## Changing the focus

This function will change the focus for the CytoSmartOpenAPI object.
Every image taken after this function will have the new focus.

The focus is in the range 0 until 1. (0.0 and 1.0 are valid entries)

You need to give the serial number of the device you want to target

```python
connector.set_focus(serial_number, 0.5)
img1 = connector.get_image(serial_number) # Image with focus of 0.5
connector.set_focus(serial_number, 0.7)
img2 = connector.get_image(serial_number) # Image with focus of 0.7
img3 = connector.get_image(serial_number) # Image with focus of 0.7
```

## Getting the temperature

This function returns the temperature in celsius of the device.

You need to give the serial number of the device you want to target

```python
temperature = connector.get_temperature(serial_number)
```

## Change activate camera (fluorescence)

To use fluorescence you will need change the active camera.
The camera can be set to 3 different values, RED, GREEN, or BRIGHTFIELD.
This will only work if your device is a fl device otherwise only BRIGHTFIELD is available.

```python
connector.set_active_camera(serial_number, "RED")
connector.set_active_camera(serial_number, "GREEN")
connector.set_active_camera(serial_number, "BRIGHTFIELD")
```

## Change camera setting

Each camera has its own settings.
Not all settings are available for BRIGHTFIELD.

- exposure: The time in milliseconds the camera is detecting light. (Lux and Exact from Omni use flash duration)
- gain: The multiplication of the camera. (Fluo only)
  If very little light goes into the camera sensor make sure the gain is high.
- brightness: Strength of the led when it is on (Fluo only)
- focus_offset: the difference in focus between brightfield and fluo.
  If focus is set to 0.4 and focus_offset for RED is set to 0.1 RED focus is 0.5 (Fluo only)

```python
connector.set_camera_settings(serial_number, "RED", 500, gain=30, brightness=5000)
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
```

## Change flash duration (Omni only)

The omni cannot change the exposure time but can change the time the led is one.
This can be done with set_flash_duration.
It will set the duration between 40 and 250 μs.

```python
connector.set_flash_duration(serial_number, duration=120)
```

If you do NOT have an omni use set_camera_settings.

## Getting a z-stack

This function will return a list of [`pillow images`](https://pillow.readthedocs.io/en/stable/reference/Image.html).
Each image will be at a different focus level.

This code will create a z-stack of 6 images.
The focuses of these images will be [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

You need to give the serial number of the device you want to target

```python
list_of_imgs = connector.get_z_stack(serial_number, num_img = 6, start_focus = 0.5, stop_focus = 1)
```

## Change stage (Omni only)

To change the position of the omni stage (camera, led, arm, ect.) give the new position in mm.

- Position x in mm
- Position y in mm
- Time in seconds it can wait till it arrives (default 60)

```python
connector.move_stage(serial_number, 100, 100, 60)
```

After this the normal process for obtaining and changing cameras applies.

## Get stage position (Omni only)

If you need to know where the stage is use get_position.
This also works if the omni moved without a move_stage command (e.q. when it goes to sleep).

```python
print(connector.get_position(serial_number))
```

## Changing zoom modes

There are 2 zoom modes: "IN" and "OUT".
While zoomed in the resolution is higher but the ROI is smaller, zoomed out has a higher ROI but a lower resolution.

Changing this will change it for every image or z-stack taken afterwards.

You need to give the serial number of the device you want to target

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
connector.set_liveview(serial_number, True) # in the browser you can see the image being updated
connector.set_liveview(serial_number, False) # Led of device turns off till you take a picture
```

## Developers

Developers of the CytoSmartOpenAPI please look at the [`developers readme`](README_DEV.md)

## Credits

- Tom Nijhof
- Nora
- Tessa
