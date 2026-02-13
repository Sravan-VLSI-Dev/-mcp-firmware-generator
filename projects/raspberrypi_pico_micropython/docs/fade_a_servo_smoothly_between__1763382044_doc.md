
# Fade a Servo Smoothly Between 0 and 180 Degrees Every 2 Seconds Using PWM on GP15

This code fades a servo smoothly between 0 and 180 degrees every 2 seconds using PWM on GPIO pin 15. It uses the machine library to control the PWM signal and the time module to manage delays.

## Purpose

The purpose of this code is to demonstrate how to use PWM to control a servo motor and fade it smoothly between two angles using a while loop. The code will run continuously and update the servo's position every 2 seconds.

## Setup

Before running this code, you will need to set up a few things:

1. Connect a servo motor to GPIO pin 15 on your microcontroller.
2. Import the necessary libraries:
	* `import machine` for controlling the PWM signal.
	* `import time` for managing delays.
3. Initialize the PWM object with the desired frequency (in this case, 50 Hz).
4. Set up a while loop to run continuously and update the servo's position every 2 seconds.

## Loop

The loop will run continuously and update the servo's position every 2 seconds. It will use the `machine.PWM()` object to control the PWM signal and adjust its duty cycle (the ratio of high to low time) to achieve the desired angle.

Here is an example of how the loop might look:
```
while True:
    for i in range(0, 180, 2):
        pwm.duty_cycle(i * 0.5)
        time.sleep_ms(1000)
```
This code will fade the servo smoothly between 0 and 180 degrees every 2 seconds using PWM on GPIO pin 15. The `range()` function is used to generate a list of angles (in this case, 0, 2, 4, ..., 180) and the `for` loop will iterate through this list and update the servo's position for each angle in the list. The `time.sleep_ms()` function is used to delay the execution of the code by 1 second (1000 milliseconds) after each iteration.

## GPIO Pins

This code uses GPIO pin 15 as the output pin for the servo motor. You will need to configure this pin in your microcontroller's GPIO settings before running the code.

## Libraries

This code uses the `machine` library and the `time` library from Micropython. You will need to import these libraries before running the code.

## Usage

To use this code, simply copy and paste it into your MicroPython editor or IDE and run it on your microcontroller. The servo motor should be connected to GPIO pin 15 and the code will fade the servo smoothly between 0 and 180 degrees every 2 seconds using PWM.