# TI Deep Learning (TIDL) API with mjpg-streamer

Demo project: https://beagleboard.org/+1ee263

See https://training.ti.com/texas-instruments-deep-learning-tidl-overview

See also /usr/share/ti/examples/tidl

# Setup

Make sure the mjpg-streamer with opencv support and TIDL library with
examples are installed:

```
sudo apt update
sudo apt install -y ti-tidl mjpg-streamer-opencv-python
```

# Execution notes

Select the "C or C++ (Beagle Makefile)" runner in the Run Configuration window.

Default user password is 'temppwd'. You'll need to type it in the Run Configuration window.

You can open the viewer window using "BeagleBone->MJPG-Streamer".
