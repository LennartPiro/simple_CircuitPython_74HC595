# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import simple_74hc595

sr = simple_74hc595.stateful_74hc595(board.GP2, board.GP3, goard.GP4)

# Create the pin objects in a list
pins = [sr.get_pin(n) for n in range(8)]

while True:
    for _ in range(2):  # Run the chase animation twice
        for enabled_pin in range(len(pins)):
            for pin_number, pin in enumerate(pins):
                if pin_number == enabled_pin:
                    pin.value = True
                else:
                    pin.value = False
                time.sleep(0.01)
    for _ in range(3):  # Run the blink animation three times
        for pin in pins:
            pin.value = True
        time.sleep(0.5)
        for pin in pins:
            pin.value = False
        time.sleep(0.5)
