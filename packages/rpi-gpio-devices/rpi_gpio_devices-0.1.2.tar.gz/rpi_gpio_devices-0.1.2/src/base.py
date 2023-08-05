from datetime import datetime
import RPi.GPIO as gpio


class BaseDevice(object):
    """
    Base class for other devices or classes

    -:param gpiomode: Gpio pin numbering mode. "board" or "bcm"
    -:param gpiowarnings: Gpio configuration warnings
    -:param verbose: Verbose mode
    """
    def __init__(self, gpiomode="board", gpiowarnings=False, verbose=False):
        self.verbose = verbose
        # GPIO basic settings
        if gpiomode == "board":
            gpio.setmode(gpio.BOARD)
        elif gpiomode == "bcm":
            gpio.setmode(gpio.BCM)
        gpio.setwarnings(gpiowarnings)

    def message(self, val):
        """ Print messages if device is in verbose mode """
        if self.verbose:
            print(val)

    def cleanup(self):
        """ Cleanup GPIOs """
        self.message("Cleanup GPIOs")
        gpio.cleanup()


class SwitchableDevice(BaseDevice):
    """ Device that can be switched on or off

    -:param power: Pin used for powering the device
    """
    def __init__(self, power, **kwargs):
        super().__init__(**kwargs)
        self.on = False # Device is on or off
        self.turned_on_at = False # When the device was turned on
        self.power = power
        if power:
            gpio.setup(power, gpio.OUT)

    def is_on(self):
        """ True if device is on """
        return self.on

    def is_off(self):
        """ True if device is off """
        return not self.on

    def turn_on(self):
        """ Turn on the device """
        if self.is_on():
            return
        self.message("Device turned on")
        self.on = True
        gpio.output(self.power, 1)

    def turn_off(self):
        """ Turn off the device """
        if self.is_off():
            return
        self.message("Device turned off")
        self.on = False
        gpio.output(self.power, 0)

    def toggle(self):
        """ Toggle device """
        if self.is_off():
            self.turn_on()
        elif self.is_on():
            self.turn_off()

    def ontime(self):
        """ Calculate the ontime if the device is on """
        if self.is_off():
            return 0
        difference = datetime.now() - self.turned_on_at
        ontime = int(difference.total_seconds() / 60)
        self.message("Ontime {} minute(s)".format(ontime))
        return ontime


class PWMDevice(SwitchableDevice):
    """ Device that can be controlled with PWM signals

    -:param power: Pin used for giving power supply to the fan
    -:param pwm: Pin used for pwm control
    -:param frequency: Frequency used for the pwm signal
    """
    def __init__(self, power, pwm, frequency=100, **kwargs):
        super().__init__(power, **kwargs)
        self.frequency = frequency
        self.duty_cycle = 0 # Duty cycle between 0.0 and 100.0
        self.pwm = False
        if pwm:
            gpio.setup(pwm, gpio.OUT)
            self.pwm = gpio.PWM(pwm, self.frequency)

    def turn_on(self):
        """ Turn on the power and pwm on the lowest setting """
        if self.is_on():
            return
        self.message("Device turned on")
        self.duty_cycle = 0
        self.turned_on_at = datetime.now()
        if self.pwm:
            self.pwm.start(0)
        if self.power:
            gpio.output(self.power, 1)
        self.on = True

    def turn_off(self):
        """ Turn off the power and pwm """
        if self.is_off():
            return
        self.message("Device turned off")
        self.duty_cycle = 0
        self.turned_on_at = False
        if self.pwm:
            self.pwm.stop()
        if self.power:
            gpio.output(self.power, 0)
        self.on = False

    def set_duty_cycle(self, percent):
        """ Set duty cycle.

        -:param percent: Duty cycle between 0% and 100%
        """
        if not self.pwm:
            raise ValueError("No pin provided for outputting PWM signal")
        if percent == 0:
            self.turn_off()
            return
        if self.is_off():
            self.turn_on()
        elif self.duty_cycle == percent:
            return
        self.message("Duty cycle set to {}%".format(percent))
        self.duty_cycle = percent
        # If the desired speed is very low, convert it, because some fans doesn`t run on lowest speed with 1%
        if 0.1 <= percent <= 1:
            percent = 0
        self.pwm.ChangeDutyCycle(percent)
