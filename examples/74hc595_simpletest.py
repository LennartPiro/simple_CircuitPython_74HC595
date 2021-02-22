# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import simple_74hc595

sr = simple_74hc595.stateful_74hc595(board.GP2, board.GP3, goard.GP4)

pin1 = sr.get_pin(1)

while True:
    pin1.value = True
    time.sleep(1)
    pin1.value = False
    time.sleep(1)
