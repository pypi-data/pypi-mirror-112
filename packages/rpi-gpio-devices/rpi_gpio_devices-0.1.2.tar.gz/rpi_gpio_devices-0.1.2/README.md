# rpi-gpio-devices

Control Raspberry Pi gpio pins more easily.

This module provides an abstraction layer to control connected devices
(fans, switches, LEDs, buttons) more easily with ready to use device classes and functions.

It uses the [RPi.GPIO](https://pypi.org/project/RPi.GPIO) module to control the GPIO pins.
Currently this is the recommended module to use for archlinuxarm, but it only provides
basic functions to manipulate the pins.

## Installation

`pip install rpi-gpio-devices`

[pypi](https://pypi.org/project/rpi-gpio-devices)

## Few examples

#### Automatic fan control based on CPU temp
``` py
from time import sleep
from rpi_gpio_devices import Fan


# Basic usage
pwm_fan = Fan(power=29, sense=35, pwm=33)

try:
    while True:
        pwm_fan.auto_set()
except KeyboardInterrupt:
    pwm_fan.cleanup()
```

#### Set LED brightness with PWM
``` py
from time import sleep
from rpi_gpio_devices import PWMLED


PWMLED1 = PWMLED(33)

PWMLED1.set_brightness(50)
sleep(2)
PWMLED1.set_brightness(100)
sleep(2)
PWMLED1.set_brightness(0)
# PWMLED1.turn_off() # Or simply just turn it off

PWMLED1.cleanup()
```

#### Check if a button is pressed
``` py
from time import sleep
from rpi_gpio_devices import Button


Button1 = Button(11)

try:
    while True:
        if Button1.is_pressed():
            print('Button1 is pressed!')
        sleep(0.5)
except KeyboardInterrupt:
    Button1.cleanup()
```

More in the [examples](https://github.com/danieltodor/rpi-gpio-devices/tree/master/examples)
directory.
