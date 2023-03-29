History
-------
1.3.1 (2023-03-29)
------------------
- Renaming to AxionVueOpenAPI

1.3.0 (2022-08-25)
------------------
- Add open_liveview
- Add do_autofocus
- Add listener to autofocus change
- Bugfix: set_focus. Make sure camera_setting is completed before setting the focus

1.2.0 (2022-06-27)
------------------
- Update server to support Omni
- Add move stage
- Add get position
- Add set flash duration
- Add mandatory turning off of warranty
- Check for connection loss and reconnect is closed
- Check for sleeping device

1.1.1 (2022-06-29)
------------------
- Update documentation

1.1.0 (2021-12-03)
------------------
- Add change camera settings
- Add set activate camera (brightfield, red-fluo, or green-fluo)
- Change focus: 
    make sure focus always happens in brightfield camera mode
    Add sleep after changing to focus so camera can move to new position
- Update to new Cytosmart app

1.0.4 (2021-04-15)
------------------
- Update Pillow
- Fix installation requirements

1.0.3 (2021-11-22)
------------------
- Update requirements of websocket and websocket-client to include version 1
- Check if app is open before starting a new one

1.0.2 (2021-04-15)
------------------
- Update pillow
- Update license to ACADEMIC PUBLIC LICENSE

1.0.1 (2021-01-14)
------------------
- Added support for LUX3 FL
- Bugfix: toggle liveview when change zoom level

1.0.0 (2020-09-15)
------------------
- Added multi lux support
- Changed output from numpy array to pillow
- Require serial number with function to get information
- Add get_temperature

0.1.2 (2020-06-30)
------------------
- Rename failing to pinging in print statement

0.1.1 (2020-06-11)
------------------
- Update documentation
- Make setup.py fit for PyPI
 
0.1.0 (2020-05-20)
------------------
- Update lux server to latest version

0.0.3 (2020-03-30)
------------------
- bugfix: files were not copied into package on linux

0.0.2 (2020-03-24)
------------------
- Bugfix: stop waiting for response after sending a message

0.0.1 (2020-03-16)
------------------

- Add function: Copy the luxconnector 
- Add function: focus change option
- Add function: z-stack
- Bugfix: add lux app to manifest

0.0.0 (2020-03-13)
------------------

Copied basic package a start of luxconnector
