# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`simple_74hc595`
====================================================

CircuitPython driver for 74HC595 shift register.

* Author(s): Kattni Rembor, Tony DiCola

Implementation Notes
--------------------

**Hardware:**

"* `74HC595 Shift Register - 3 pack <https://www.adafruit.com/product/450>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import digitalio

__version__ = "1.0.0-auto.0"
__repo__ = "https://github.com/LennartPiro/simple_CircuitPython_74HC595"


class simple_74hc595:
    def __init__(self, data_pin, clock_pin, latch_pin):
        def is_inout_pin(pin):
            return hasattr(pin, 'direction') and hasattr(pin, 'value')

        if is_inout_pin(data_pin):
            self.data_pin = data_pin
        else:
            self.data_pin = digitalio.DigitalInOut(data_pin)
        self.data_pin.direction = digitalio.Direction.OUTPUT

        if is_inout_pin(clock_pin):
            self.clock_pin = clock_pin
        else:
            self.clock_pin = digitalio.DigitalInOut(clock_pin)
        self.clock_pin.direction = digitalio.Direction.OUTPUT

        if is_inout_pin(latch_pin):
            self.latch_pin = latch_pin
        else:
            self.latch_pin = digitalio.DigitalInOut(latch_pin)
        self.latch_pin.direction = digitalio.Direction.OUTPUT

        self.end_push_values()

    def push_bit(self, value):
        self.clock_pin.value = False
        self.data_pin.value = value
        self.clock_pin.value = True

    def begin_push_values(self):
        self.clock_pin.value = False
        self.latch_pin.value = False
        self.clock_pin.value = True

    def end_push_values(self):
        self.clock_pin.value = False
        self.latch_pin.value = True
        self.clock_pin.value = True

    def write_byte(self, value):
        assert 0 <= value <= 255
        self.begin_push_values()
        for i in range(8):
            self.push_bit((value >> (7 - i)) & 1)
        self.end_push_values()

    def write_byte_array(self, values):
        assert len(values) == 8
        self.begin_push_values()
        for v in values:
            self.push_bit(v)
        self.end_push_values()


class DigitalInOut:
    # """Digital input/output of the 74HC595.  The interface is exactly the
    # same as the ``digitalio.DigitalInOut`` class, however note that by design
    # this device is OUTPUT ONLY!  Attempting to read inputs or set
    # direction as input will raise an exception.
    # """

    def __init__(self, pin_number, shift_register_74hc595):
        # """Specify the pin number of the shift register (0...7) and
        # ShiftRegister74HC595 instance.
        # """
        self._pin = pin_number
        self._shift_register = shift_register_74hc595

    # kwargs in switch functions below are _necessary_ for compatibility
    # with DigitalInout class (which allows specifying pull, etc. which
    # is unused by this class).  Do not remove them, instead turn off pylint
    # in this case.
    def switch_to_output(self, value=False, **kwargs):
        self.direction = digitalio.Direction.OUTPUT
        self.value = value

    def switch_to_input(self, **kwargs):
        raise RuntimeError("Digital input not supported.")

    @property
    def value(self):
        return self._shift_register.read_bit(self._pin)

    @value.setter
    def value(self, val):
        self._shift_register.write_bit(self._pin, val)

    @property
    def direction(self):
        return digitalio.Direction.OUTPUT

    @direction.setter
    def direction(self, val):
        if val != digitalio.Direction.OUTPUT:
            raise RuntimeError("Digital input not supported.")

    @property
    def pull(self):
        return None

    @pull.setter
    def pull(self, val):
        if val is not None:
            raise RuntimeError("Pull-up and pull-down not supported.")


class stateful_74hc595(simple_74hc595):
    def __init__(self, data_pin, clock_pin, latch_pin, initial_state=0):
        super().__init__(
            data_pin, clock_pin, latch_pin
        )
        self.pin_state = initial_state
        self.update()

    def update(self):
        self.write_byte(self.pin_state)

    def write_bit(self, pin_number, value):
        assert 0 <= pin_number <= 7
        if value:
            self.pin_state |= 1 << pin_number
        else:
            self.pin_state ^= self.pin_state & (1 << pin_number)
        self.update()

    def read_bit(self, pin_number):
        assert 0 <= pin_number <= 7
        return (self.pin_state & (1 << pin_number)) > 0

    def get_pin(self, pin):
        # """Convenience function to create an instance of the DigitalInOut class
        # pointing at the specified pin of this 74HC595 device .
        # """
        assert 0 <= pin <= 7
        return DigitalInOut74HC595(pin, self)
