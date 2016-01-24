#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import math, opc, time

w = 12
d = 8
h = 60
numLEDs = w * d * h
client = opc.Client('localhost:8080')

index = 0
while True:
    pixels = [(0, 0, 0)] * numLEDs
    pixels[index % numLEDs] = (255, 255, 255)
    client.put_pixels(pixels)
    index += 1
