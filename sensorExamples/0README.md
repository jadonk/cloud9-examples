# Sensor Examples
Here are examples of how to interface common sensors and input devices.

Script            | Description
------            | -----------
accelerometer.js  | This example reads values from Sparkfun’s ADXL335 3-axis accelerometer. 
hc-sr04-ultraSonic.js | Shows how to use a HC-SR04 Ultrasonic Range Sensor
joystick.js       | The Analog 2-axis Thumb Joystick allows you to easily mount a PSP/Xbox-like thumb joystick to your project.
motionSensor.js   | The PIR Motion Sensor, or Passive Infrared Sensor, is a sensor that takes a snapshot of the room and it detects changes in heat.
potentiometer.js  | A specific voltage can be sent to the AIN1 channel using a potentiometer. 
rotaryEncoder.js  | How do use a rotary encoder (_quadrature encoder_) connected to the Bone's eQEP ports
servo.js          | The Micro Servo Motor can rotate 180 degrees and is usually used in applications such as robotics, CNC machinery, or automated manufacturing.
tempHumidity.js   | Uses si7021 to red temp and humidity via I2C. 
tempPressure.js   | The BMP085 is a readily available pressure/temperature sensor using I2C. 
ultrasonic.js     | The LV-MaxSonar-EZ2 High Performance Sonar Range Finder provides very short to long-range detection and ranging, in an incredibly small package. 

# Pins used

Demo                 |     | Output | Input | Pull | I2C
----                 | --- | ------ | ----- | ---- | ---
accelerometer.js     | AIN |
hc-sr04-ultraSonic.js|     | P9_15  | P9_17 | 
i2cTemp.js           |     |        |       |      | P9_19, P9_20
joystick.js          | AIN |        | P9_18 | up   |
motionSensor.js      |     | P9_15  | P9_29 |      |
potentiometer.js     | AIN |
rotaryEncoder.js     |     |        | P8_33, P8_35 | down
servo.js             | PWM |
tempHumidity.js      |     |        |       |      | P9_19, P9_20
tempPressure.js      |     |        |       |      | P9_19, P9_20
ultrasonic.js        | AIN |