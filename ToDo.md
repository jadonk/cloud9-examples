# To Do

- [x] README.md
- [ ] fix prudebug

- [ ] AI/README.md - add tidl
- [ ] AI/pru/blinkExternalLED.c  Fails every other time on AI due to exporting P9_25
- [x] AI/pru/shared.c - Using bitflip.c
- [ ] AI/blinkLED.js  - Need bonescript mappings for AI
- [ ] AI/analongINSync.js - Where are the analog ins?

- [ ] AI/tidl/classification.tidl.cpp

## Black/0README.md
- [ ] Blink.ino
- [ ] blinky.rb
- [ ] pwmTest.sh
- [ ] shiftout.js

- [ ] Black/0README.md - Fix .js files
- [x] Black/pru/0README.md
- [ ] Black/pru/blinkR30.c - How to config-pin P9_29 pruout
- [ ] Black/pru/bitflip.c - need /dev/uio
- 

# PocketBeagle
- [x] PocketBeagle/pru/ring.pru0.c
- [ ] PocketBeagle/pru/bitflip.c - need /dev/uio
- [ ] PocketBeagle/0README.md
- [ ] PocketBeagle/servoMotor.js - Test
- [ ] PocketBeagle/sensorTag.js  - Test
- [ ] PocketBeagle/blinkLED.py   - ImportError: No module named Adafruit_BBIO.GPIO
- [ ] PocketBeagle/pushbutton.js - attachInterrupt err = attachInterrupt: requires Epoll module
- [ ] PocketBeagle/input.js      - very slow to respond
- [ ] PocketBeagle/input2.js     - very slow to respond too
- [ ] Test PocketBeagle/pru/ring.pru0.c
- 

# Migration from Bone101 (simple BoneScript + hardware examples)
- [ ] Accelerometer - Don't have one to test
- [x] hc-sr04 - tested Black/AI
- [ ] i2cTemp - Black only.  Needs testing - Doesn't work
- [x] Joystick - tested Black/AI
- [x] PIRMotionSensors - tested Black/AI
- [x] Potentiometer - tested Black/AI
- [x] rotaryEncoder - tested Black/AI
- [x] Servo - Figure out PWM on AI
- [ ] Humidity and temp, si7021 - Same interface as BMP085, but gives wrong values
- [ ] Pressure and temperature sensor - BMP085 - tested Black/AI - Needs udev rule
- [x] Ultrasonic Sensor - tested Black
