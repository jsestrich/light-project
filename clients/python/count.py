#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import math, opc, time

w = 12
d = 8
h = 60
numLEDs = w * d * h
client = opc.Client('localhost:8080')

pixels = [(0, 0, 0)] * numLEDs
for x in range(w):
    for y in range(d):
        for z in range(h):
            i = z + x * h + y * w * h
            pixels[i] = (
                255 if x == z - 20 else 0,
                255 if y == z - 20 else 0,
                0
            )
client.put_pixels(pixels)
