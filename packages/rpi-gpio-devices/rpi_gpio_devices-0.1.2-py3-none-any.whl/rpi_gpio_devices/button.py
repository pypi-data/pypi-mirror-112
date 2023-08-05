import time
import RPi.GPIO as gpio
from .base import BaseDevice


class Button(BaseDevice):
    """ Button device

    -:param pin: Which pin is connected to the button
    -:param debounce_time: Debounce time when checking button state (ms)
    -:param polarity: When you press the button, will the pin be connected to LOW or HIGH?
    """
    def __init__(self, pin, debounce_time=200, polarity='LOW', **kwargs):
        super().__init__(**kwargs)
        self.debounce_time = debounce_time / 1000
        self.polarity = polarity
        self.pin = pin
        gpio.setup(pin, gpio.IN, pull_up_down={'HIGH': gpio.PUD_DOWN, 'LOW': gpio.PUD_UP}[polarity])

    def is_pressed(self):
        """ True if the button is pressed """
        def HIGH(pin):
            if gpio.input(pin):
                return True
            return False
        def LOW(pin):
            if not gpio.input(pin):
                return True
            return False
        test = {'HIGH': HIGH, 'LOW': LOW}[self.polarity]

        if test(self.pin):
            time.sleep(self.debounce_time)
            if test(self.pin):
                self.message('Button is pressed!')
                return True
        return False
